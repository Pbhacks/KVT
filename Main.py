from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from plyer import notification
import joblib
import re
import webbrowser

# Load models and preprocessing objects
vectorizer = joblib.load('model/vectorizer.pkl')

models = {
    'RandomForest': joblib.load('model/RandomForest_model.pkl'),
    'GradientBoosting': joblib.load('model/GradientBoosting_model.pkl'),
    'NaiveBayes': joblib.load('model/NaiveBayes_model.pkl'),
    'SVM': joblib.load('model/SVM_model.pkl'),
    'LogisticRegression': joblib.load('model/LogisticRegression_model.pkl'),
    'AdaBoost': joblib.load('model/AdaBoost_model.pkl'),
    'MLP': joblib.load('model/MLP_model.pkl')
}

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Main content
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Logo
        layout.add_widget(Image(source='assets/tokyo.jpg', size_hint=(1, 1), height=300, width=300))
        
        # Welcome Label
        welcome_label = Label(text="Welcome to the Tokyo 2025 Olympics Anti-Phishing App", font_size='20sp')
        content_layout.add_widget(welcome_label)
        
        # Navigation buttons
        btn_guide = Button(text="Phishing Detection", size_hint=(1, 0.2))
        btn_guide.bind(on_press=self.goto_guide)
        content_layout.add_widget(btn_guide)
        
        
        
        layout.add_widget(content_layout)
        self.add_widget(layout)
    
    def goto_guide(self, instance):
        self.manager.current = 'guide'

    def on_quit(self, instance):
        App.get_running_app().stop()

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add the image to the layout
        layout.add_widget(Image(source='assets/tokyo1.jpeg', size_hint=(1, 1), height=300, width=300))
        
        # Add buttons for different menu options
        btn_settings = Button(text="Settings", size_hint_y=None, height=40, on_press=self.goto_settings)
        btn_user_education = Button(text="User Education", size_hint_y=None, height=40, on_press=self.goto_anti_phishing)
        btn_quit = Button(text="Quit", size_hint_y=None, height=40, on_press=self.on_quit)
        
        layout.add_widget(btn_settings)
        layout.add_widget(btn_user_education)
        layout.add_widget(btn_quit)
        
        self.add_widget(layout)

    def goto_settings(self, instance):
        self.manager.current = 'settings'
        
    def goto_anti_phishing(self, instance):
        self.manager.current = 'anti-phishing'

    def go_back(self, instance):
        self.manager.current = 'home'
    
    def on_quit(self, instance):
        App.get_running_app().stop()
class GuideScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.email_input = TextInput(hint_text='Paste Email Content Here', multiline=True, size_hint=(1, 0.7))
        layout.add_widget(self.email_input)
        
        analyze_button = Button(text='Analyze Email', size_hint=(1, 0.1))
        analyze_button.bind(on_press=self.analyze_email)
        layout.add_widget(analyze_button)
        
        self.result_label = Label(text='', size_hint=(1, 0.1))
        layout.add_widget(self.result_label)
        
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
    def analyze_email(self, instance):
        email_content = self.email_input.text
        features = vectorizer.transform([email_content])
        
        # Select model for prediction (for simplicity, using RandomForest here)
        model = models['RandomForest']
        prediction = model.predict(features)
        is_phishing = prediction[0] == 1
        
        url_phishing = False
        urls = re.findall(r'(https?://\S+)', email_content)
        for url in urls:
            if "phishing" in url:  # Simplified URL check, replace with actual logic
                url_phishing = True
                break
        
        if is_phishing or url_phishing:
            self.result_label.text = 'This email is likely a phishing attempt!'
            notification.notify(title="Phishing Alert", message="Potential phishing email detected!")
        else:
            self.result_label.text = 'This email appears to be safe.'
    
    def go_back(self, instance):
        self.manager.current = 'home'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.image = Image(source='assets/settingsbg.jpg', allow_stretch=True)
        self.image.size_hint = (1, 1)
        layout.add_widget(self.image)

        # Automation settings
        automation_label = Label(text="Enable Automation", size_hint=(1, 0.2))
        layout.add_widget(automation_label)
        
        self.automation_button = Button(text="Disabled", size_hint=(1, 0.2))
        self.automation_button.bind(on_press=self.toggle_automation)
        layout.add_widget(self.automation_button)
        
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)
    
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

class AntiPhishingInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Anti-phishing information
        info_text = (
            "[b][size=24]How to Prevent Phishing Attacks!?[/size][/b]\n\n"
            "[size=18]1. Be Skeptical of Unknown Senders:[/size]\n"
            "   - Always be cautious when receiving emails or messages from unknown sources. "
            "   Phishing emails often come from seemingly legitimate addresses but are designed to "
            "   trick you into revealing sensitive information.\n\n"
            
            "[size=18]2. Verify Links Before Clicking:[/size]\n"
            "   - Hover over links to see the actual URL before clicking. If the URL looks suspicious or "
            "   does not match the content of the message, avoid clicking on it.\n\n"
            
            "[size=18]3. Avoid Sharing Personal Information:[/size]\n"
            "   - Do not provide personal or financial information in response to unsolicited requests. "
            "   Legitimate organizations will never ask for sensitive information via email or text.\n\n"
            
            "[size=18]4. Use Strong, Unique Passwords:[/size]\n"
            "   - Use strong passwords for your accounts and avoid reusing passwords across multiple sites. "
            "   Consider using a password manager to generate and store complex passwords.\n\n"
            
            "[size=18]5. Enable Two-Factor Authentication (2FA):[/size]\n"
            "   - Enable 2FA on your accounts when available. This adds an extra layer of security by requiring "
            "   a second form of verification in addition to your password.\n\n"
            
            "[size=18]6. Keep Software Updated:[/size]\n"
            "   - Regularly update your operating system, browsers, and applications to ensure you have the latest "
            "   security patches and fixes.\n\n"
            
            "[size=18]7. Educate Yourself and Others:[/size]\n"
            "   - Stay informed about the latest phishing tactics and educate those around you about how to recognize "
            "   and avoid phishing attempts.\n\n"
            
            "[size=18]8. Report Suspicious Activity:[/size]\n"
            "   - If you receive a suspicious email or message, report it to your email provider or the relevant authority. "
            "   Many organizations have dedicated channels for reporting phishing attempts.\n\n"
            
            "[size=18]9. Be Wary of Urgent or Threatening Language:[/size]\n"
            "   - Phishing emails often use urgent or threatening language to create a sense of panic and compel you to act quickly. "
            "   Take a moment to consider if the message is legitimate before responding.\n\n"
            
            "[size=18]10. Check for Grammar and Spelling Errors:[/size]\n"
            "    - Many phishing emails contain grammar and spelling mistakes. While not all suspicious emails have these errors, "
            "    their presence can be a red flag.\n\n"
            
            "[size=18]11. Look for Generic Greetings:[/size]\n"
            "    - Legitimate organizations usually address you by your name. Be cautious if the email uses generic greetings like "
            "    'Dear Customer' or 'Dear User'.\n\n"
            
            "[size=18]12. Don't Download Attachments from Unknown Sources:[/size]\n"
            "    - Avoid downloading attachments from unknown or unexpected sources. They may contain malware that can compromise your system.\n\n"
            
            "[size=18]13. Secure Your Wi-Fi Network:[/size]\n"
            "    - Ensure your home or office Wi-Fi network is secure with a strong password to prevent unauthorized access. "
            "    Avoid using public Wi-Fi for accessing sensitive information.\n\n"
            
            "[size=18]14. Use Antivirus and Anti-Malware Software:[/size]\n"
            "    - Install and regularly update antivirus and anti-malware software to protect your devices from malicious attacks.\n\n"
            
            "[size=18]15. Be Cautious with Pop-Ups:[/size]\n"
            "    - Be wary of pop-up windows asking for personal information or urging you to download software. Legitimate organizations "
            "    typically do not request sensitive information this way.\n\n"
            
            "[size=18]16. Verify the Source:[/size]\n"
            "    - If you receive an email or message that seems suspicious but appears to come from a known source, contact the organization "
            "    directly using contact information from their official website, not the contact details provided in the message.\n\n"
            
            "[size=18]17. Use Browser Filters:[/size]\n"
            "    - Enable browser filters to help detect and block known phishing websites. Most modern browsers have built-in features to alert you to phishing attempts.\n\n"
            
            "[size=18]18. Be Aware of Spear Phishing:[/size]\n"
            "    - Spear phishing targets specific individuals or organizations. These attacks are often more sophisticated and personalized. "
            "    Be extra cautious if you receive an unexpected email or message that appears to be highly personalized.\n\n"
            
            "[size=18]19. Regularly Monitor Your Accounts:[/size]\n"
            "    - Regularly check your bank and credit card statements for any unauthorized transactions. Report any suspicious activity immediately.\n\n"
            
            "[size=18]20. Stay Informed About Security Practices:[/size]\n"
            "    - Keep yourself updated with the latest security practices and phishing trends. Awareness and knowledge are key defenses against phishing attacks.\n\n"
            
            "[size=18]By following these best practices, you can help protect yourself from falling victim to phishing attacks.[/size]"
        )

        # Add information as a label with markup enabled
        info_label = Label(text=info_text, font_size='12sp', halign='left', valign='top', size_hint_y=None, markup=True)
        info_label.bind(size=info_label.setter('text_size'))
        
        # Set the height of the label to be based on its content
        info_label.bind(texture_size=info_label.setter('size'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(info_label)
        
        layout.add_widget(scroll_view)

        video_links = [
            ("Understanding Phishing Attacks", "https://youtu.be/XBkzBrXlle0"),
            ("How to Recognize Phishing Emails", "https://youtu.be/o0btqyGWIQw"),
            
        ]
        
        for title, url in video_links:
            video_button = Button(text=title, size_hint=(1, 0.1))
            video_button.bind(on_press=lambda instance, url=url: self.open_video(url))
            layout.add_widget(video_button)
        
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'home'

    def open_video(self, url):
        webbrowser.open(url)

class BottomNavBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1

        home_button = Button(text='Home')
        home_button.bind(on_press=self.goto_home)
        self.add_widget(home_button)

        menu_button = Button(text='Menu')
        menu_button.bind(on_press=self.goto_menu)
        self.add_widget(menu_button)

    def goto_home(self, instance):
        App.get_running_app().screen_manager.current = 'home'

    def goto_menu(self, instance):
        App.get_running_app().screen_manager.current = 'menu'

class AntiPhishingApp(App):
    def build(self):
        self.icon = 'assets/olympics_logo.jpg'
        self.title = 'Tokyo 2025 Olympics Anti-Phishing App'

        self.screen_manager = ScreenManager()

        self.home_screen = HomeScreen(name='home')
        self.screen_manager.add_widget(self.home_screen)

        self.menu_screen = MenuScreen(name='menu')
        self.screen_manager.add_widget(self.menu_screen)

        self.guide_screen = GuideScreen(name='guide')
        self.screen_manager.add_widget(self.guide_screen)

        self.settings_screen = SettingsScreen(name='settings')
        self.screen_manager.add_widget(self.settings_screen)

        self.anti_phishing_info_screen = AntiPhishingInfoScreen(name='anti-phishing')
        self.screen_manager.add_widget(self.anti_phishing_info_screen)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.screen_manager)
        main_layout.add_widget(BottomNavBar())

        return main_layout

if __name__ == '__main__':
    AntiPhishingApp().run()
