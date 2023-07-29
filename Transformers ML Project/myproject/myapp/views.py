from django.shortcuts import render
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Replace 'user/marian-finetuned-en-to-fr' with your private model identifier
MODEL_ID = 'Vidyuth/marian-finetuned-kde4-en-to-fr'
# Replace 'YOUR_HUGGING_FACE_API_TOKEN' with your actual Hugging Face API token
TOKEN = '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'

# Load the model with authentication
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID, use_auth_token=TOKEN)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_auth_token=TOKEN)

# Define your translation logic or model integration here
def translate_text(english_text):
    inputs = tokenizer.encode("translate English to French: " + english_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(inputs, max_length=1024, num_beams=5, early_stopping=True)
    french_translation = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove unwanted characters and leading/trailing whitespaces
    french_translation = french_translation.replace("traduire l'anglais en français & #160;:", "").strip()
    return french_translation

def main_page(request):
    return render(request, 'main.html')

def translate_page(request):
    if request.method == 'POST':
        english_text = request.POST.get('english_text', '')
        french_translation = translate_text(english_text)
        return render(request, 'translate.html', {'translation': french_translation})
    
    return render(request, 'translate.html')
# myapp/views.py

MODEL_ID_SUMMARIZE = 'Vidyuth/mt5-small-finetuned-amazon-en-es'
# Replace 'YOUR_HUGGING_FACE_API_TOKEN' with your actual Hugging Face API token
TOKEN_SUMMARIZE = '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'

from django.shortcuts import render
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the summarization model with authentication
model_summarize = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID_SUMMARIZE, use_auth_token=TOKEN_SUMMARIZE)
tokenizer_summarize = AutoTokenizer.from_pretrained(MODEL_ID_SUMMARIZE, use_auth_token=TOKEN_SUMMARIZE)

def summarize_text(input_text):
    # Tokenize the input text
    inputs = tokenizer_summarize.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
    # Generate the summary
    summary_ids = model_summarize.generate(inputs, max_length=150, min_length=50, num_beams=4, early_stopping=True)
    # Decode the summary and return
    summary = tokenizer_summarize.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def summarize_page(request):
    if request.method == 'POST':
        # Get the user input from the form
        text_to_summarize = request.POST.get('text_to_summarize', '')

        # Perform the summarization task using the Hugging Face model
        summary = summarize_text(text_to_summarize)

        return render(request, 'summarize.html', {'summary': summary})

    return render(request, 'summarize.html')

from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from django.shortcuts import render
import torch 
MODEL_ID_QNA = 'Vidyuth/bert-finetuned-squad'
TOKEN_QNA = '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'
model_qna = AutoModelForQuestionAnswering.from_pretrained(MODEL_ID_QNA, use_auth_token=TOKEN_QNA, ignore_mismatched_sizes=True)
tokenizer_qna = AutoTokenizer.from_pretrained(MODEL_ID_QNA, use_auth_token=TOKEN_QNA)

def answer_question(context, question):
    # Tokenize the input context and question
    inputs = tokenizer_qna.encode_plus(question, context, return_tensors="pt", max_length=512, truncation=True)
    # Get the model outputs
    with torch.no_grad():
        outputs = model_qna(**inputs)
    # Extract the start and end logits
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits
    # Find the start and end positions with the maximum logits
    answer_start = torch.argmax(start_logits)
    answer_end = torch.argmax(end_logits) + 1
    # Decode the tokens and get the answer
    answer = tokenizer_qna.decode(inputs["input_ids"][0][answer_start:answer_end])
    return answer

def qnsans_page(request):
    if request.method == 'POST':
        # Get the user input from the form
        context = request.POST.get('context_text', '')
        question = request.POST.get('question', '')
        # Perform the question answering task using the Hugging Face model
        answer = answer_question(context, question)
        return render(request, 'qnsans.html', {'answer': answer})

    return render(request, 'qnsans.html')

def game_page(request):
    return render(request, 'game.html')


