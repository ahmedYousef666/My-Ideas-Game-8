from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.spinner import Spinner
from kivy.config import Config
from kivy.logger import Logger
import csv
import os
from kivy.core.audio import SoundLoader
import sys

# ========== إعدادات مسبقة لضمان ظهور النافذة ==========
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'window_state', 'visible')
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'  # للأجهزة القديمة
Logger.setLevel('INFO')  # لرؤية رسائل التصحيح

class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.current_level = 0
        self.padding = 20
        self.spacing = 15
        self.sounds = [None] * 5
        self.user_data = []
        
        # ========== عناصر الواجهة المعدلة ==========
        self.level_label = Label(
            text=f"المستوى: {self.current_level +1} #المستوى_{self.current_level +1}", 
            font_size=28,
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1)  # لون أسود
        )
        self.add_widget(self.level_label)
        
        # منطقة الرسم مع خلفية ملونة
        self.canvas_widget = Widget(size_hint=(1, 0.4))
        with self.canvas_widget.canvas:
            Color(0.95, 0.95, 0.95, 1)  # رمادي فاتح
            self.bg_rect = Rectangle(pos=self.canvas_widget.pos, size=self.canvas_widget.size)
        self.add_widget(self.canvas_widget)
        
        # الجملة النصية مع هاشتاج
        self.sentence_label = Label(
            text="", 
            font_size=22,
            size_hint=(1, 0.15),
            halign='center',
            color=(0, 0, 0, 1)  # لون أسود
        )
        self.add_widget(self.sentence_label)
        
        # خانات النص مع حدود واضحة
        self.summary_input = TextInput(
            text="تلخيص الفكرة: ",
            size_hint=(1, 0.15),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            multiline=True,
            font_size=18
        )
        self.add_widget(self.summary_input)
        
        self.application_input = TextInput(
            text="تطبيقات الفكرة: ",
            size_hint=(1, 0.15),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            multiline=True,
            font_size=18
        )
        self.add_widget(self.application_input)
        
        # أزرار التحكم بتصميم محسن
        control_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        self.prev_button = Button(
            text="السابق",
            background_color=(0.2, 0.6, 1, 1),  # أزرق
            font_size=18
        )
        self.prev_button.bind(on_press=self.prev_level)
        control_layout.add_widget(self.prev_button)
        
        self.next_button = Button(
            text="إنهاء المستوى",
            background_color=(0.3, 0.8, 0.3, 1),  # أخضر
            font_size=18
        )
        self.next_button.bind(on_press=self.next_level)
        control_layout.add_widget(self.next_button)
        
        self.sound_button = Button(
            text="إضافة صوت",
            background_color=(1, 0.5, 0, 1),  # برتقالي
            font_size=18
        )
        self.sound_button.bind(on_press=self.show_sound_chooser)
        control_layout.add_widget(self.sound_button)
        
        self.export_button = Button(
            text="تصدير البيانات",
            background_color=(0.8, 0.2, 0.8, 1),  # بنفسجي
            font_size=18
        )
        self.export_button.bind(on_press=self.export_data)
        control_layout.add_widget(self.export_button)
        
        self.add_widget(control_layout)
        
        # ========== تهيئة البيانات ==========
        self.sentences = [
            "#المستوى_1: التعلم أساس النجاح.",
            "#المستوى_2: الصبر مفتاح الفرج.",
            "#المستوى_3: الابتكار يقود التقدم.",
            "#المستوى_4: العمل الجماعي يبني الأمم.",
            "#المستوى_5: بدون هدف لن تصل إلى شيء."
        ]
        
        self.update_display()
        self.draw_level()
    
    def update_display(self):
        self.level_label.text = f"المستوى: {self.current_level +1} #المستوى_{self.current_level +1}"
        self.sentence_label.text = self.sentences[self.current_level]
        
        if self.sounds[self.current_level]:
            self.sounds[self.current_level].play()
    
    def draw_level(self):
        self.canvas_widget.canvas.clear()
        with self.canvas_widget.canvas:
            # خلفية
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=self.canvas_widget.pos, size=self.canvas_widget.size)
            
            # رسم النقاط
            for i in range(len(self.sentences)):
                if i <= self.current_level:
                    Color(0, 1, 0)  # أخضر للمكتمل
                else:
                    Color(1, 0, 0)  # أحمر للغير مكتمل
                
                Ellipse(pos=(i * (Window.width-100)/len(self.sentences) + 50, 50), size=(30, 30))
                Color(0, 0, 0)
                Label(text=str(i + 1), pos=(i * (Window.width-100)/len(self.sentences) + 60, 55))
            
            # الشخصية
            Color(0, 0, 1)  # أزرق
            Ellipse(pos=(self.current_level * (Window.width-100)/len(self.sentences) + 50, 150), 
                   size=(50, 50))
    
    def next_level(self, instance):
        self.save_current_data()
        if self.current_level < len(self.sentences) - 1:
            self.current_level += 1
            self.update_display()
            self.draw_level()
        else:
            self.show_popup("تهانينا!", "لقد أكملت جميع المستويات!")
    
    def prev_level(self, instance):
        if self.current_level > 0:
            self.save_current_data()
            self.current_level -= 1
            self.update_display()
            self.draw_level()
    
    def save_current_data(self):
        data = {
            "level": self.current_level + 1,
            "hashtag": f"#المستوى_{self.current_level +1}",
            "sentence": self.sentences[self.current_level],
            "summary": self.summary_input.text.replace("تلخيص الفكرة: ", ""),
            "application": self.application_input.text.replace("تطبيقات الفكرة: ", ""),
            "sound_file": self.sounds[self.current_level].source if self.sounds[self.current_level] else ""
        }
        
        if len(self.user_data) <= self.current_level:
            self.user_data.append(data)
        else:
            self.user_data[self.current_level] = data
    
    def show_sound_chooser(self, instance):
        # Modified for Android compatibility
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE])
            
            from android.storage import primary_external_storage_path
            from os.path import join
            default_path = join(primary_external_storage_path(), 'Download')
            
            # Use a simpler approach for Android
            self.show_popup("Sound Selection", 
                           "Please place sound files in the Download folder and restart the app.")
            return
            
        # Original desktop implementation
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(filters=['*.mp3', '*.wav', '*.ogg'])
        content.add_widget(file_chooser)
        
        def load_sound(selected):
            try:
                if selected:
                    sound = SoundLoader.load(selected[0])
                    if sound:
                        self.sounds[self.current_level] = sound
                        self.show_popup("نجاح", "تم تحميل الصوت بنجاح!")
                        popup.dismiss()
            except Exception as e:
                self.show_popup("خطأ", f"تعذر تحميل الصوت: {str(e)}")
        
        btn_layout = BoxLayout(size_hint=(1, 0.1))
        btn_cancel = Button(text='إلغاء')
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        btn_load = Button(text='تحميل')
        btn_load.bind(on_press=lambda x: load_sound(file_chooser.selection))
        
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_load)
        content.add_widget(btn_layout)
        
        popup = Popup(title='اختر ملف صوتي', content=content, size_hint=(0.9, 0.9))
        popup.open()
    
    def export_data(self, instance):
        self.save_current_data()
        
        # Modified for Android compatibility
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
            
            from android.storage import primary_external_storage_path
            export_dir = join(primary_external_storage_path(), 'Download')
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
        else:
            export_dir = os.getcwd()
        
        content = BoxLayout(orientation='vertical', spacing=10)
        spinner = Spinner(
            text='اختر صيغة التصدير',
            values=('CSV', 'Excel'),
            size_hint=(1, 0.2),
            font_size=18
        )
        
        export_btn = Button(
            text='تصدير', 
            size_hint=(1, 0.2),
            background_color=(0, 0.7, 0, 1)  # أخضر داكن
        )
        cancel_btn = Button(
            text='إلغاء', 
            size_hint=(1, 0.2),
            background_color=(0.8, 0, 0, 1)  # أحمر
        )
        
        def do_export(instance):
            if spinner.text == 'CSV':
                self.export_to_csv(export_dir)
            elif spinner.text == 'Excel':
                self.export_to_excel(export_dir)
            popup.dismiss()
        
        export_btn.bind(on_press=do_export)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        content.add_widget(spinner)
        content.add_widget(export_btn)
        content.add_widget(cancel_btn)
        
        popup = Popup(title='تصدير البيانات', content=content, size_hint=(0.8, 0.5))
        popup.open()
    
    def export_to_csv(self, export_dir=''):
        try:
            filename = os.path.join(export_dir, 'game_data.csv')
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(['المستوى', 'الهاشتاج', 'الجملة النصية', 
                               'تلخيص الفكرة', 'تطبيقات الفكرة', 'ملف الصوت'])
                
                for data in self.user_data:
                    writer.writerow([
                        data['level'],
                        data['hashtag'],
                        data['sentence'],
                        data['summary'],
                        data['application'],
                        data['sound_file']
                    ])
            
            self.show_popup("نجاح", f"تم تصدير البيانات إلى {filename}")
        except Exception as e:
            self.show_popup("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def export_to_excel(self, export_dir=''):
        try:
            import xlsxwriter
            filename = os.path.join(export_dir, 'game_data.xlsx')
            
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            
            # تنسيق العناوين
            header_format = workbook.add_format({
                'bold': True,
                'align': 'center',
                'bg_color': '#4F81BD',
                'font_color': 'white'
            })
            
            headers = ['المستوى', 'الهاشتاج', 'الجملة النصية', 
                      'تلخيص الفكرة', 'تطبيقات الفكرة', 'ملف الصوت']
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
                worksheet.set_column(col, col, len(header) + 5)
            
            # كتابة البيانات
            for row, data in enumerate(self.user_data, start=1):
                worksheet.write(row, 0, data['level'])
                worksheet.write(row, 1, data['hashtag'])
                worksheet.write(row, 2, data['sentence'])
                worksheet.write(row, 3, data['summary'])
                worksheet.write(row, 4, data['application'])
                worksheet.write(row, 5, data['sound_file'])
            
            workbook.close()
            self.show_popup("نجاح", f"تم تصدير البيانات إلى {filename}")
        except Exception as e:
            self.show_popup("خطأ", f"حدث خطأ أثناء التصدير: {str(e)}")
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, font_size=20),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class GameApp(App):
    def build(self):
        # Check platform
        global platform
        platform = 'android' if 'ANDROID_BOOTLOGO' in os.environ else 'desktop'
        
        # Set window properties
        Window.clearcolor = (1, 1, 1, 1)  # خلفية بيضاء
        
        # Load Arabic font if available
        if platform == 'android':
            from kivy.core.text import LabelBase
            from android.storage import app_storage_path
            fonts_dir = app_storage_path()
            
            # We'll add the font file in the buildozer.spec
            try:
                LabelBase.register(name="Arabic", 
                                  fn_regular=os.path.join(fonts_dir, "NotoKufiArabic-Regular.ttf"))
                # Apply to all labels and buttons
                from kivy.core.text import Label as CoreLabel
                CoreLabel.register('Arabic', 'fonts/NotoKufiArabic-Regular.ttf')
            except Exception as e:
                Logger.warning(f"Could not load Arabic font: {e}")
        
        return GameScreen()

if __name__ == '__main__':
    try:
        GameApp().run()
    except Exception as e:
        Logger.exception("حدث خطأ غير متوقع")
        sys.exit(1)
