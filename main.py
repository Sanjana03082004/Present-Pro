from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import video_pred

app = FastAPI()

class VideoProcessingRequest(BaseModel):
    input_video_file_path: str
    conf: float

@app.post("/process_video/")
def process_video(request: VideoProcessingRequest):
    input_video_file_path = request.input_video_file_path
    conf = request.conf

    print(f"Input Video File Path: {input_video_file_path}")
    print(f"Confidence: {conf}")

    label_file,video_file_path, = video_pred.run_detection(
        weights='best.pt',
        source=input_video_file_path,
        conf=conf,
        save_txt=True,
        save_conf=True,
        save_crop=True,
        project='results_dir',
        name=uuid.uuid4().hex 
    )
    
    results = {}
    results['labels'] = video_pred.get_results_summary(label_file)
    results['output_file_path'] = video_file_path
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
