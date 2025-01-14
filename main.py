import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pyttsx3
from kivy.graphics import Color, Rectangle

kivy.require('2.3.1')  # Make sure to install Kivy v2.3.1 or higher

# Language Config File
LANGUAGE = {
    'en': {
        'height': "Enter your height (m):",
        'weight': "Enter your weight (kg):",
        'age': "Enter your age:",
        'gender': "Select your gender:",
        'calculate': "Calculate BMI",
        'bmi_result': "Your BMI is: ",
        'bmi_category': "BMI Category: ",
        'unit': "Select unit for height:",
        'male': "Male",
        'female': "Female",
        'error_message': "Please enter valid values for height, weight, and age."
    },
    'bn': {
        'height': "আপনার উচ্চতা (মি) দিন:",
        'weight': "আপনার ওজন (কেজি) দিন:",
        'age': "আপনার বয়স দিন:",
        'gender': "আপনার লিঙ্গ নির্বাচন করুন:",
        'calculate': "বিএমআই হিসাব করুন",
        'bmi_result': "আপনার বিএমআই হল: ",
        'bmi_category': "বিএমআই শ্রেণী: ",
        'unit': "উচ্চতার জন্য একক নির্বাচন করুন:",
        'male': "পুরুষ",
        'female': "মহিলা",
        'error_message': "উচ্চতা, ওজন এবং বয়সের জন্য বৈধ মান দিন।"
    }
}

# Set the language here
LANG = LANGUAGE['en']

def calculate_bmi(weight, height, age, gender):
    try:
        weight = float(weight)
        height = float(height)
        age = int(age)

        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be greater than 0")

        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"

        return bmi, category
    except ValueError:
        return None, None


class BMICalculatorApp(App):
    def build(self):
        self.title = "BMI Calculator"
        layout = FloatLayout()

        self.bmi_label = Label(text=LANG['bmi_result'], size_hint=(None, None), width=250, font_size='20sp', color=(1, 1, 1, 1), padding=(10, 10))
        self.bmi_category_label = Label(text=LANG['bmi_category'], size_hint=(None, None), width=250, font_size='20sp', color=(1, 1, 1, 1), padding=(10, 10))
        self.error_label = Label(text=LANG['error_message'], size_hint=(None, None), width=300, font_size='16sp', color=(1, 0, 0, 1))

        self.height_input = TextInput(hint_text=LANG['height'], multiline=False, input_filter='float', size_hint=(None, None), width=350, height=40)
        self.weight_input = TextInput(hint_text=LANG['weight'], multiline=False, input_filter='float', size_hint=(None, None), width=350, height=40)
        self.age_input = TextInput(hint_text=LANG['age'], multiline=False, input_filter='int', size_hint=(None, None), width=350, height=40)

        self.gender_spinner = Spinner(text=LANG['gender'], values=[LANG['male'], LANG['female']], size_hint=(None, None), width=350, height=40)
        self.height_unit_spinner = Spinner(text=LANG['unit'], values=["m", "cm", "inches"], size_hint=(None, None), width=350, height=40)

        self.calculate_button = Button(text=LANG['calculate'], size_hint=(None, None), width=250, height=50, background_color=(0.2, 0.6, 1, 1), font_size='18sp')
        self.calculate_button.bind(on_press=self.calculate_bmi)

        # Center align widgets on the layout
        self.height_input.pos_hint = {'center_x': 0.5, 'center_y': 0.8}
        self.height_unit_spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.75}
        self.weight_input.pos_hint = {'center_x': 0.5, 'center_y': 0.65}
        self.age_input.pos_hint = {'center_x': 0.5, 'center_y': 0.55}
        self.gender_spinner.pos_hint = {'center_x': 0.5, 'center_y': 0.45}
        self.calculate_button.pos_hint = {'center_x': 0.5, 'center_y': 0.35}
        self.bmi_label.pos_hint = {'center_x': 0.5, 'center_y': 0.25}
        self.bmi_category_label.pos_hint = {'center_x': 0.5, 'center_y': 0.2}
        self.error_label.pos_hint = {'center_x': 0.5, 'center_y': 0.1}

        # Add background color to text inputs
        self.height_input.background_color = (0.9, 0.9, 0.9, 1)
        self.weight_input.background_color = (0.9, 0.9, 0.9, 1)
        self.age_input.background_color = (0.9, 0.9, 0.9, 1)

        # Add background color to gender and unit spinners
        self.gender_spinner.background_color = (0.9, 0.9, 0.9, 1)
        self.height_unit_spinner.background_color = (0.9, 0.9, 0.9, 1)

        # Add a soft border radius to inputs and buttons
        self.height_input.border_radius = [10]
        self.weight_input.border_radius = [10]
        self.age_input.border_radius = [10]
        self.calculate_button.border_radius = [15]

        # Add widgets to the layout
        layout.add_widget(self.height_input)
        layout.add_widget(self.height_unit_spinner)
        layout.add_widget(self.weight_input)
        layout.add_widget(self.age_input)
        layout.add_widget(self.gender_spinner)
        layout.add_widget(self.calculate_button)
        layout.add_widget(self.bmi_label)
        layout.add_widget(self.bmi_category_label)
        layout.add_widget(self.error_label)

        # Bind the height unit spinner to update the height input's hint text
        self.height_unit_spinner.bind(text=self.update_height_hint)

        return layout

    def update_height_hint(self, spinner, text):
        if text == "m":
            self.height_input.hint_text = LANG['height']
        elif text == "cm":
            self.height_input.hint_text = "Enter your height (cm):"
        elif text == "inches":
            self.height_input.hint_text = "Enter your height (inches):"

    def calculate_bmi(self, instance):
        weight = self.weight_input.text
        height = self.height_input.text
        age = self.age_input.text
        gender = self.gender_spinner.text
        unit = self.height_unit_spinner.text

        if weight == '' or height == '' or age == '':
            self.bmi_label.text = ''
            self.bmi_category_label.text = ''
            self.error_label.text = LANG['error_message']
            return

        # Convert height to meters if needed
        if unit == 'cm':
            height = float(height) / 100
        elif unit == 'inches':
            height = float(height) * 0.0254
        else:
            height = float(height)  # height in meters

        bmi, category = calculate_bmi(weight, height, age, gender)

        if bmi is not None and category is not None:
            self.bmi_label.text = f"{LANG['bmi_result']} {bmi:.2f}"
            self.bmi_category_label.text = f"{LANG['bmi_category']} {category}"
            self.error_label.text = ''
        else:
            self.bmi_label.text = ''
            self.bmi_category_label.text = ''
            self.error_label.text = LANG['error_message']
            self.play_audio(LANG['error_message'])

    def play_audio(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


if __name__ == "__main__":
    BMICalculatorApp().run()
