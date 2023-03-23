import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
import speech_recognition as sp

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SpeechToTextGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1920x1080")
        self.title("Speech-to-Text")
        self.font = ("Comic Sans MS", 20, "bold")
        self.font1 = ("Comic Sans MS", 24, "bold")

        label = ctk.CTkLabel(self, text="~~~~~~~~~~~ PRESS THE SPEAK BUTTON TO START TALKING ~~~~~~~~~~~", font=self.font1, text_color="magenta")
        label.pack(padx=10, pady=10)

        self.text_area = ScrolledText(self, font=self.font, width=70, height=20, bg="lavender", wrap="word")
        self.text_area.pack(padx=10, pady=10)

        speak_button = ctk.CTkButton(self, text="Speak", font=self.font, height=60, command=self.recognize_speech)
        speak_button.pack(padx=10, pady=10)

        save_button = ctk.CTkButton(self, text="Save Text", font=self.font, height=60, command=self.save_text)
        save_button.pack(padx=10, pady=10)

        self.recognizer = sp.Recognizer()

    def recognize_speech(self):
        with sp.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                recognized_text = self.recognizer.recognize_google(audio)
                if self.text_area.get("1.0", ctk.END).strip() == "":
                    recognized_text = recognized_text.capitalize()
                else:
                    last_char = self.text_area.get("end-2c", ctk.END).strip()
                    if last_char == "." or last_char == "?":
                        recognized_text = recognized_text.capitalize()
                    else:
                        recognized_text = recognized_text.lower()
                    recognized_text = " " + recognized_text

                self.text_area.insert(ctk.END, recognized_text)
                self.text_area.see(ctk.END)
            except Exception as e:
                print('Error : ' + str(e))

    def save_text(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(self.text_area.get("1.0", ctk.END))


if __name__ == '__main__':
    app = SpeechToTextGUI()
    app.mainloop()

