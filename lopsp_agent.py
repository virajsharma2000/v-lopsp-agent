import time
import ollama

# Base prompt template
BASE_TASK = "You are managing a long-term project to write a poem one line at a time. \
Each time I ask, give the next line and how many seconds I should wait before I ask again. \
Respond in the format: {'next_line': '<line>', 'next_delay_seconds': <seconds>} \
also tell me the reason why that amount of time was selected as"

# Start interaction loop
def run_scheduler():
    history = []
    prompt = BASE_TASK

    while True:
        # Send prompt to Ollama
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': BASE_TASK},
            {'role': 'user', 'content': prompt}
        ])
        print(response)
        try:
            # Extract model response
            output = eval(response['message']['content'])
            print("📝 Next line:", output['next_line'])
            print("⏱️ Waiting for", output['next_delay_seconds'], "seconds...\n")

            history.append(output)
            prompt = f"The last line was: '{output['next_line']}'"

            time.sleep(output['next_delay_seconds'])

        except Exception as e:
            print("Error in response or parsing:", e)
            break

if __name__ == "__main__":
    run_scheduler()
