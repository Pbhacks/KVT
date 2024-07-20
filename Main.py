import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from plyer import notification
import joblib

# Load models and preprocessing objects
vectorizer = joblib.load('model/vectorizer.pkl')

models = {
    'RandomForest': joblib.load('model/RandomForest_model.pkl'),
    'GradientBoosting': joblib.load('model/GradientBoosting_model.pkl'),
    'NaiveBayes': joblib.load('model/NaiveBayes_model.pkl'),
    'SVM': joblib.load('model/SVM_model.pkl')
}

class HomeScreen(Screen):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Logo
        layout.add_widget(Image(source='assets/tokyo.jpg'))
        
        # Welcome Label
        welcome_label = Label(text="Welcome to the Tokyo 2025 Olympics Anti-Phishing App", font_size='20sp')
        layout.add_widget(welcome_label)
        
        # Navigation buttons
        btn_guide = Button(text="Phishing Detection", size_hint=(1, 0.2))
        btn_guide.bind(on_press=self.goto_guide)
        layout.add_widget(btn_guide)
        
        btn_settings = Button(text="Settings", size_hint=(1, 0.2))
        btn_settings.bind(on_press=self.goto_settings)
        layout.add_widget(btn_settings)
        
        return layout

    def goto_guide(self, instance):
        self.manager.current = 'guide'
        
    def goto_settings(self, instance):
        self.manager.current = 'settings'

class GuideScreen(Screen):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.email_input = TextInput(hint_text='Paste Email Content Here', multiline=True, size_hint=(1, 0.7))
        layout.add_widget(self.email_input)
        
        analyze_button = Button(text='Analyze Email', size_hint=(1, 0.1))
        analyze_button.bind(on_press=self.analyze_email)
        layout.add_widget(analyze_button)
        
        self.result_label = Label(text='', size_hint=(1, 0.2))
        layout.add_widget(self.result_label)
        
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        return layout
    
    def analyze_email(self, instance):
        email_content = self.email_input.text
        features = vectorizer.transform([email_content])
        
        model = models['RandomForest']  # Set your default model
        prediction = model.predict(features)
        is_phishing = prediction[0] == 1
        
        if is_phishing:
            self.result_label.text = 'This email is likely a phishing attempt!'
        else:
            self.result_label.text = 'This email appears to be safe.'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class SettingsScreen(Screen):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Automation settings
        automation_label = Label(text="Enable Automation", size_hint=(1, 0.2))
        layout.add_widget(automation_label)
        
        self.automation_button = Button(text="Disabled", size_hint=(1, 0.2))
        self.automation_button.bind(on_press=self.toggle_automation)
        layout.add_widget(self.automation_button)
        
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        return layout
    
    def toggle_automation(self, instance):
        if self.automation_button.text == "Disabled":
            self.automation_button.text = "Enabled"
            self.start_automation()
        else:
            self.automation_button.text = "Disabled"
            # Stop automation if needed
            pass
    
    def start_automation(self):
        # Request SMS permissions and start monitoring
        self.request_permissions()
        # This is a placeholder. Implement the background monitoring in Android
        pass
    
    def request_permissions(self):
        # Code to request SMS and other permissions
        pass
    
    def go_back(self, instance):
        self.manager.current = 'home'

class AntiPhishingApp(App):
    def build(self):
        self.title = 'Anti-Phishing App for Tokyo 2025'
        self.screen_manager = ScreenManager()
        
        home_screen = HomeScreen(name='home')
        home_screen.add_widget(home_screen.build())
        self.screen_manager.add_widget(home_screen)
        
        guide_screen = GuideScreen(name='guide')
        guide_screen.add_widget(guide_screen.build())
        self.screen_manager.add_widget(guide_screen)
        
        settings_screen = SettingsScreen(name='settings')
        settings_screen.add_widget(settings_screen.build())
        self.screen_manager.add_widget(settings_screen)
        
        return self.screen_manager

if __name__ == '__main__':
    AntiPhishingApp().run()