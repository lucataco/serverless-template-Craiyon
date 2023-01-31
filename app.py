import PIL
import torch
import base64
from PIL import Image
from io import BytesIO
from min_dalle import MinDalle
from IPython.display import display, update_display

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model

    model = MinDalle(
        dtype=getattr(torch, "float32"),
        device='cuda',
        is_mega=True, 
        is_reusable=True
    )


# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    prompt = model_inputs.get('prompt', None)
    if prompt == None:
        return {'message': "No prompt provided"}

    image = model.generate_image(
        text=prompt,
        seed=-1,
        grid_size=1,
        is_seamless=False,
        temperature=1,
        top_k=256,
        supercondition_factor=32,
        is_verbose=False
    )
    buffered = BytesIO()
    image.save(buffered,format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the results as a dictionary
    return {'image_base64': image_base64}
