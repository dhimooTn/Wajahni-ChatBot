import os
import google.generativeai as genai
from dotenv import load_dotenv
import customtkinter as ctk
from PIL import Image


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8191,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "Create a chatbot named 'Wajahni' that specializes in providing the best orientation "
        "for university careers. The chatbot should:\n\n"
        "- Analyze users' Baccalaureate marks and compare them with university programs' admission requirements.\n"
        "- Use the data from the provided 'Orientation Guide 2024' to match users with appropriate university options.\n"
        "- Provide clear and personalized advice based on:\n"
        "  - User preferences.\n"
        "  - Eligibility criteria for different fields of study as outlined in the guide.\n"
        "  - Recommendations for improving their selection chances.\n"
        "- Be interactive, user-friendly, and provide responses in both Arabic and English.\n"
        "- Include links or references to resources such as official orientation websites or contact points for more information.\n"
        "- Ensure the chatbot can simulate realistic and empathetic interactions while delivering accurate, helpful, and engaging advice."
    ),
)


chat_session = model.start_chat(history=[])


ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  


app = ctk.CTk()
app.title("Wajahni Chatbot")
app.geometry("900x700")


logo_image = ctk.CTkImage(Image.open("logoOr.jpg").resize((100, 100)))


header_frame = ctk.CTkFrame(app, corner_radius=10)
header_frame.pack(pady=10, padx=10, fill="x")


logo_label = ctk.CTkLabel(header_frame, text="", image=logo_image)
logo_label.pack(side="left", padx=20)


title_label = ctk.CTkLabel(
    header_frame,
    text="Wajahni - Your University Orientation Assistant",
    font=("Arial", 24, "bold"),
    text_color="#2B78E4",
)
title_label.pack(side="left", padx=10)


chat_frame = ctk.CTkFrame(app, corner_radius=10)
chat_frame.pack(fill="both", expand=True, padx=20, pady=10)


conversation_history = ctk.CTkTextbox(
    chat_frame, wrap="word", font=("Arial", 14), state="disabled"
)
conversation_history.pack(padx=10, pady=10, fill="both", expand=True)


def display_message(sender, message):
    conversation_history.configure(state="normal")
    if sender == "bot":
        
        conversation_history.insert("end", "Wajahni: ", "bot_label")
        conversation_history.insert("end", f"{message}\n", "message_text")
    elif sender == "user":
        
        conversation_history.insert("end", "You: ", "user_label")
        conversation_history.insert("end", f"{message}\n", "message_text")
    conversation_history.insert("end", "\n", "spacing")  
    conversation_history.configure(state="disabled")
    conversation_history.see("end")  

def send_message():
    user_input = user_entry.get().strip()
    if user_input:
        display_message("user", user_input)
        try:
            response = chat_session.send_message(user_input)
            bot_response = response.text
            display_message("bot", bot_response)
        except Exception as e:
            display_message("bot", f"Error: {str(e)}")
        user_entry.delete(0, "end")


input_frame = ctk.CTkFrame(app, corner_radius=10)
input_frame.pack(pady=10, padx=10, fill="x")

user_entry = ctk.CTkEntry(
    input_frame, placeholder_text="Type your message...", font=("Arial", 14)
)
user_entry.pack(side="left", padx=10, fill="x", expand=True)

send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    command=send_message,
    fg_color="#4CAF50",
    hover_color="#45a049",
    font=("Arial", 14),
)
send_button.pack(side="right", padx=10)


conversation_history.tag_config("bot_label", foreground="pink")  
conversation_history.tag_config("user_label", foreground="yellow")  
conversation_history.tag_config("message_text", foreground="white")  
conversation_history.tag_config("spacing", foreground="")  


footer_label = ctk.CTkLabel(
    app,
    text="Powered by Ahmed Dhia Boukhdhir - Mohamed Aziz Turki - Adem Manai",
    font=("Arial", 12),
    text_color="#888",
)
footer_label.pack(pady=10)


app.mainloop()
