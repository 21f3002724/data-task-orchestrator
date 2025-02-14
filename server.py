from fastapi import FastAPI, HTTPException, Query
from task_executor import execute_task
from file_reader import read_file

# Initialize FastAPI app
app = FastAPI()


@app.post("/run")
def run_task(task: str = Query(..., description="Task description")):
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")
    result = execute_task(task)
    return result


@app.get("/read")
def read_file_endpoint(path: str = Query(..., description="File path to read")):
    if not path:
        raise HTTPException(status_code=400, detail="File path is required")
    return read_file(path)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
