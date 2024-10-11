import json
import logging
from textprocessor.process_manager import ProcessManager
from textprocessor.task_runners import ConcurrentTaskRunner
from textprocessor.utils import transform_mark_data, merge_markups, markup_text

from concurrent.futures import ThreadPoolExecutor, as_completed

class ProcessingPipeline:
    def __init__(self, pm: ProcessManager):
        self.pm = pm

    def process_with_llm(self, processor, prompts_data, metadata):
        runner = ConcurrentTaskRunner()
        results = dict()

        def process_task(markup_id, prompt_config):
            try:
                payload = {'prompt_config': json.loads(prompt_config)}
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
                return None

            try:
                if markup_id == 1:
                    res = self.pm.runWith(processor, payload)
                    return res
                elif markup_id == 2:
                    res = self.pm.runWith(processor, payload)
                    self.result['llm_notes'] = res
            except Exception as e:
                logging.error(f"Error processing markup_id {markup_id}: {e}")
                return None

        for prompt_data in prompts_data:
            runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)

        markups_res = runner.run_all()
        markups = [res for res in markups_res if res is not None]

        try:
            results['llm_annotated'] = transform_mark_data(merge_markups(self.pm.getContext("text"), markups), metadata)
        except Exception as e:
            logging.error(f"Error merging markups: {e}")
            results['llm_annotated'] = None

        return results

    # def process_with_llm(pm: ProcessManager, processor, prompts_data, metadata):
    #     result = dict()
    #     final_result_markup_id_1 = None
    #     runner = ConcurrentTaskRunner()

    #     def process_task(markup_id, prompt_config, prev_res=None):
    #         try:
    #             payload = {'prompt_config': json.loads(prompt_config)}
    #             if prev_res is not None:
    #                 payload['previous_result'] = prev_res
    #         except json.JSONDecodeError as e:
    #             logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
    #             return None

    #         try:
    #             if markup_id == 1:
    #                 res = pm.runWith(processor, payload)
    #                 return res
    #             elif markup_id == 2:
    #                 res = pm.runWith(processor, payload)
    #                 result['llm_notes'] = res
    #                 return res
    #         except Exception as e:
    #             logging.error(f"Error processing markup_id {markup_id}: {e}")
    #             return None

    #     def process_markup_id_1_tasks(prompts_data):
    #         nonlocal final_result_markup_id_1  # Ensure we're using the outer variable
    #         prev_res = None
    #         for prompt_data in prompts_data:
    #             if prompt_data.markup_id == 1:
    #                 prev_res = process_task(prompt_data.markup_id, prompt_data.prompt_config, prev_res)
    #                 if prev_res is not None:
    #                     final_result_markup_id_1 = prev_res
    #         return final_result_markup_id_1

    #     # Process markup_id == 1 tasks in a separate thread
    #     with ThreadPoolExecutor() as executor:
    #         future_id_1 = executor.submit(process_markup_id_1_tasks, prompts_data)
            
    #         # Process other tasks concurrently
    #         for prompt_data in prompts_data:
    #             if prompt_data.markup_id != 1:
    #                 runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)
            
    #         # Run all concurrent tasks
    #         markups_res = runner.run_all()
    #         markups = [res for res in markups_res if res is not None]
            
    #         # Wait for the sequential tasks to complete
    #         final_result_markup_id_1 = future_id_1.result()

    #         # Combine results
    #         if final_result_markup_id_1:
    #             markups.append(final_result_markup_id_1)

    #         result['llm_annotated'] = markups  # Update to include all markups
                
    #     return result


    def process_with_nlp(self, processor, metadata):
        return markup_text(self.pm.getContext("text"), self.pm.runWith(processor), metadata)


    # def process_with_llm(pm: ProcessManager, processor, prompts_data, metadata):
    #     sequential_prompts = [data for data in prompts_data if data.markup_id == 1]
    #     concurrent_prompts = [data for data in prompts_data if data.markup_id != 1]

    #     # Define the processing task
    #     def process_task(markup_id, prompt_config, previous_result=None):
    #         try:
    #             payload = {'prompt_config': json.loads(prompt_config)}
    #             if previous_result:
    #                 payload['previous_result'] = previous_result
    #         except json.JSONDecodeError as e:
    #             logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
    #             return None

    #         try:
    #             return pm.runWith(processor, payload)
    #         except Exception as e:
    #             logging.error(f"Error processing markup_id {markup_id}: {e}")
    #             return None

    #     # Process sequential tasks using PipelineTaskRunner
    #     pipeline_runner = PipelineTaskRunner()
    #     for prompt_data in sequential_prompts:
    #         pipeline_runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)

    #     # Process concurrent tasks using ConcurrentTaskRunner
    #     concurrent_runner = ConcurrentTaskRunner()
    #     for prompt_data in concurrent_prompts:
    #         concurrent_runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)

    #     # Run both task runners concurrently
    #     # Combine results
    #     combined_results = ConcurrentTaskRunner().add_task(pipeline_runner.run_all).add_task(concurrent_runner.run_all)
    #     combined_results.extend(final_sequential_result)
        
    #     return combined_results
