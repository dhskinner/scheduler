import os
import asyncio
import schedule
import time
from threading import Thread

print("Scheduler starting... ")

# Path to the folder containing scripts
SCRIPT_FOLDER = "./scripts"  # Replace with the path to your subfolder

# Define the schedule intervals for each script (in minutes)
SCRIPT_SCHEDULE = {
    "task1.py": 30,
    "task2.py": 30,
    "task3.py": 1,
}

async def run_script_async(script_name: str):
    """Run a specific Python script asynchronously."""
    try:
        script_path = os.path.join(SCRIPT_FOLDER, script_name)
        print(f"[Async-{script_name}] Running script: {script_name}")
        
        # Run the script using subprocess
        process = await asyncio.create_subprocess_exec(
            "python", script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print(f"[Async-{script_name}] Script {script_name} ran successfully.")
            print(f"[Async-{script_name}] Output: {stdout.decode()}")
        else:
            print(f"[Async-{script_name}] Script {script_name} failed with return code {process.returncode}.")
            print(f"[Async-{script_name}] Error: {stderr.decode()}")
    except Exception as e:
        print(f"[Async-{script_name}] An error occurred while running {script_name}: {e}")

def schedule_script_with_async_thread(script_name: str, interval: int):
    """Schedule a script to run in an asynchronous thread."""
    async def job():
        await run_script_async(script_name)

    def run_async_job():
        asyncio.run(job())

    # Schedule the job to run in its own thread
    def thread_job():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(job())

    schedule.every(interval).minutes.do(lambda: Thread(target=thread_job).start())
    print(f"Scheduled {script_name} to run every {interval} minutes asynchronously.")

def schedule_scripts():
    """Schedule each script based on its defined interval."""
    for script_name, interval in SCRIPT_SCHEDULE.items():
        if script_name in os.listdir(SCRIPT_FOLDER):
            schedule_script_with_async_thread(script_name, interval)

# Schedule the scripts
schedule_scripts()

print("Scheduler started. Press Ctrl+C to stop.")

# Main loop to keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(1)
