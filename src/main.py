import nest_asyncio
import gradio as gr
from typing import Tuple
import asyncio
import aiohttp
from research_agents import *
from api_clients import *
# from threading import Event


nest_asyncio.apply()

async def process_link(session, link, user_query, query_used, log_messages, model_config):
    """Helper function to process a single link"""
    page_text = await fetch_webpage_text_async(session, link)
    if not page_text:
        log_messages.append(f"❌ Failed to fetch content from: {link}")
        return None
        
    is_useful = await is_page_useful_async(session, user_query, page_text, model_config)
    if is_useful == "Yes":
        log_messages.append(f"✅ Found useful content from: {link}")
        log_messages.append(f"   Query used: {query_used}")
        return page_text[:10000]  # Limit context size
    else:
        log_messages.append(f"⛔ Content not relevant from: {link}")
        return None

async def get_new_search_queries_async(session, user_query, all_search_queries, aggregated_contexts, model_config):
    """Generate new search queries based on findings"""
    if not aggregated_contexts:
        return []
        
    context_summary = "\n".join(aggregated_contexts[-2:])  # Use recent contexts
    new_queries_prompt = (
        "Based on the findings so far and the original query, determine if more research is needed. "
        "If yes, generate up to 2 new search queries that would help fill gaps in our research. "
        "If no, indicate that the research is complete.\n\n"
        f"Original Query: {user_query}\n\n"
        f"Previous Queries: {all_search_queries}\n\n"
        f"Recent Findings:\n{context_summary}"
    )
    
    messages = [
        {"role": "system", "content": "You are a research query generator. Respond with either a Python list of new search queries or 'COMPLETE' if no more research is needed."},
        {"role": "user", "content": new_queries_prompt}
    ]
    
    response = await call_openrouter_async(session, messages, model_config)
    if "COMPLETE" in response:
        return ""
    try:
        return eval(response)
    except:
        return []

async def generate_final_report_async(session, user_query, aggregated_contexts, model_config):
    """Generate the final research report"""
    combined_context = "\n\n".join(aggregated_contexts)
    report_prompt = (
        "Based on the following research findings, generate a comprehensive "
        "report that addresses the user's query. Include key insights and "
        "maintain a professional tone.\n\nUser Query: "
        f"{user_query}\n\nResearch Findings:\n{combined_context}"
    )
    
    messages = [
        {"role": "system", "content": "You are a professional research report writer."},
        {"role": "user", "content": report_prompt}
    ]
    
    final_report = await call_openrouter_async(session, messages, model_config)
    return final_report if final_report else "Error generating final report."

async def async_research(user_query: str, iteration_limit: int, model_config: dict) -> Tuple[str, str]:
    """
    Main research routine that orchestrates the entire research process.
    
    Args:
        user_query: User's research query
        iteration_limit: Maximum number of research iterations
        
    Returns:
        Tuple of (final report, log messages)
    """
    aggregated_contexts = []
    all_search_queries = []
    log_messages = []

    async with aiohttp.ClientSession() as session:
        # Initial search query generation
        new_search_queries = await generate_search_queries_async(session, user_query, model_config)
        if not new_search_queries:
            return "No search queries were generated.", "Error: No initial queries generated."
            
        all_search_queries.extend(new_search_queries)
        log_messages.append("🔍 Initial Search Queries:")
        for q in new_search_queries:
            log_messages.append(f"   • {q}")

        iteration = 0
        while iteration < iteration_limit:
            log_messages.append(f"\n=== Iteration {iteration + 1} ===")
            iteration_contexts = []
            search_tasks = [perform_search_async(session, query) for query in new_search_queries]
            search_results = await asyncio.gather(*search_tasks)
            unique_links = {}
            for idx, links in enumerate(search_results):
                query_used = new_search_queries[idx]
                for link in links:
                    if link not in unique_links:
                        unique_links[link] = query_used

            log_messages.append(f"📚 Aggregated {len(unique_links)} unique links from this iteration.")
            link_tasks = [
                process_link(session, link, user_query, unique_links[link], log_messages, model_config)
                for link in unique_links
            ]
            link_results = await asyncio.gather(*link_tasks)
            for res in link_results:
                if res:
                    iteration_contexts.append(res)

            if iteration_contexts:
                aggregated_contexts.extend(iteration_contexts)
                log_messages.append(f"✨ Found {len(iteration_contexts)} useful contexts in this iteration.")
            else:
                log_messages.append("⚠️ No useful contexts were found in this iteration.")

            new_search_queries = await get_new_search_queries_async(
                session, user_query, all_search_queries, aggregated_contexts, model_config
            )
            if new_search_queries == "":
                log_messages.append("🎯 LLM indicated that no further research is needed.")
                break
            elif new_search_queries:
                log_messages.append("🔄 New search queries generated:")
                for q in new_search_queries:
                    log_messages.append(f"   • {q}")
                all_search_queries.extend(new_search_queries)
            else:
                log_messages.append("⚡ No new search queries provided. Ending the loop.")
                break

            iteration += 1

        log_messages.append("\n📝 Generating final report...")
        final_report = await generate_final_report_async(session, user_query, aggregated_contexts, model_config)
        return final_report, "\n".join(log_messages)

def run_research(user_query: str, iteration_limit: int = 10, model_config: dict = DEFAULT_MODEL) -> Tuple[str, str]:
    """
    Synchronous wrapper for the async research function.
    """
    return asyncio.run(async_research(user_query, iteration_limit, model_config))

def process_research(query: str, model: str, iterations: int, depth: str):
    """
    Processes the research request with depth adjustment
    """
    try:
        depth_multipliers = {"Quick": 0.5, "Standard": 1.0, "Deep": 2.0}
        adjusted_iterations = int(iterations * depth_multipliers[depth])
        
        # Get the model configuration from AVAILABLE_MODELS
        model_config = AVAILABLE_MODELS[model]
        
        # Run the research using the selected model configuration
        final_report, process_log = run_research(query, adjusted_iterations, model_config)
        
        return (
            final_report,
            process_log,
            "Status: Research Complete ✅"
        )
        
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        return (error_msg, error_msg, "Status: Error ❌")

# Create Gradio interface
def create_interface():
    """Creates a research assistant interface with model selection"""
    
    with gr.Blocks(theme=gr.themes.Soft()) as interface:
        gr.Markdown("""
        # 🔍 Open Research AI Assistant
        
        ### Decentralized AI-powered research assistant helps you gather and synthesize information on any topic using multiple models.
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Input components
                query = gr.Textbox(
                    label="Research Query",
                    placeholder="Enter your research topic or question...",
                    lines=3
                )
                
                model_selector = gr.Dropdown(
                    choices=[(v['name'], k) for k, v in AVAILABLE_MODELS.items()],
                    value=DEFAULT_MODEL,
                    label="Select AI Model"
                )
                
                with gr.Row():
                    iterations = gr.Slider(
                        minimum=1,
                        maximum=20,
                        value=10,
                        step=1,
                        label="Maximum Iterations"
                    )
                    
                    depth = gr.Radio(
                        choices=["Quick", "Standard", "Deep"],
                        value="Standard",
                        label="Research Depth"
                    )
                
                # Action buttons
                with gr.Row():
                    submit_btn = gr.Button("Begin Research", variant="primary")
                    clear_btn = gr.Button("Clear")
            
            with gr.Column(scale=1):
                gr.Markdown("""
                ### Tips for Better Results
                
                - Be specific in your query
                - Use clear, focused questions
                - Include key terms and concepts
                - Specify time periods if relevant
                """)    
                # Output components
                status = gr.Markdown("Status: Ready")
        
        report = gr.Textbox(
            label="Research Report",
            placeholder="Research results will appear here...",
            lines=15,
            show_copy_button=True
        )
        
        log = gr.Textbox(
            label="Process Log",
            lines=10,
            show_copy_button=True
        )
        
        with gr.Row():
            save_btn = gr.Button("💾 Save Report")
            export_btn = gr.Button("📤 Export as PDF")
            share_btn = gr.Button("🔗 Share")
        
        def clear_outputs():
            """Clears all output fields"""
            return "", "", "Status: Ready"
        
        # Wire up the interface
        submit_btn.click(
            fn=process_research,
            inputs=[query, model_selector, iterations, depth],
            outputs=[report, log, status]
        )
        
        clear_btn.click(
            fn=clear_outputs,
            inputs=None,
            outputs=[report, log, status]
        )
        
        return interface

# Create and launch the interface
if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=False)