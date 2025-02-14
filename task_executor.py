from fastapi import HTTPException
import subprocess
from openai import OpenAI
from datetime import datetime
import os
import urllib.request
import ssl

# LLM client setup
client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",  # Local LLM server
    api_key="sk-no-key-required",
)

# Create an unverified SSL context
ssl_context = ssl._create_unverified_context()

def execute_task(task: str):
    try:
        print("Task:::",task)
        if "install uv" in task.lower() and "run datagen.py" in task.lower():
            subprocess.run(["pip3", "install", "uv"], check=True)
            script_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
            script_path = "/tmp/datagen.py"
            
            # Download script with SSL verification disabled
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(
                script_url, context=ssl_context
            ) as response, open(script_path, "wb") as out_file:
                out_file.write(response.read())
                
            subprocess.run(
                ["python3", script_path, "21f3002724@ds.study.iitm.ac.in"], check=True
            )
            return {"message": "Task A1 completed successfully."}

        elif "format /data/format.md" in task.lower():
            subprocess.run(
                ["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True
            )
            return {"message": "Task A2 completed successfully."}

        elif "count wednesdays" in task.lower() and "/data/dates.txt" in task.lower():
            with open("/data/dates.txt", "r") as f:
                lines = f.readlines()
            count = sum(
                1
                for line in lines
                if datetime.strptime(line.strip(), "%Y-%m-%d").weekday() == 2
            )
            with open("/data/dates-wednesdays.txt", "w") as f:
                f.write(str(count))
            return {"message": "Task A3 completed successfully.", "wednesdays": count}

        else:
            # Call LLM for additional task processing
            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # Using LLM to interpret task
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI that executes automation tasks.",
                    },
                    {"role": "user", "content": task},
                ],
            )
            return {
                "message": "LLM processed the task.",
                "response": completion.choices[0].message.content,
            }

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Task execution error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid task format: {str(e)}")
