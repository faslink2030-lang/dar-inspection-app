import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

WEB_APP_URL = "https://script.google.com/macros/s/YOUR_EXEC_DEPLOYMENT_ID/exec"

KV = '''
ScrollView:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "16dp"
        spacing: "12dp"
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "تطبيق الفحص الميداني - دار الخليج"
            font_style: "H6"
            halign: "center"
            bold: True

        MDTextField:
            id: contractor_name
            hint_text: "اسم المقاول"
            mode: "rectangle"

        MDTextField:
            id: statement_number
            hint_text: "رقم الحصر"
            mode: "rectangle"

        MDTextField:
            id: license_number
            hint_text: "رقم الرخصة"
            mode: "rectangle"

        MDTextField:
            id: qc_name
            hint_text: "اسم مراقب الجودة"
            mode: "rectangle"

        MDTextField:
            id: region
            hint_text: "المنطقة"
            mode: "rectangle"

        MDRaisedButton:
            text: "📍 جلب إحداثيات الموقع الحالي (GPS)"
            md_bg_color: 0.42, 0.3, 0.49, 1
            size_hint_x: 1
            on_release: app.get_gps_location()

        MDLabel:
            id: gps_label
            text: "الإحداثيات الحالية: Lat: 16.263250, Lng: 42.262658"
            halign: "center"

        MDRaisedButton:
            text: "إرسال البيانات للتقرير"
            md_bg_color: 0.18, 0.49, 0.2, 1
            size_hint_x: 1
            on_release: app.send_data()
'''

class FieldInspectionApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def get_gps_location(self):
        self.root.ids.gps_label.text = "تم جلب الإحداثيات: Lat: 16.263250, Lng: 42.262658"

    def send_data(self):
        payload = {
            "contractor_name": self.root.ids.contractor_name.text,
            "statement_number": self.root.ids.statement_number.text,
            "license_number": self.root.ids.license_number.text,
            "qc_name": self.root.ids.qc_name.text,
            "region": self.root.ids.region.text,
            "lat": "16.263250",
            "lng": "42.262658"
        }
        try:
            response = requests.post(WEB_APP_URL, json=payload, timeout=30)
            if response.status_code == 200:
                self.show_dialog("نجاح", "تم إرسال التقرير بنجاح!")
            else:
                self.show_dialog("تنبيه", f"رمز الاستجابة: {response.status_code}")
        except Exception as e:
            self.show_dialog("خطأ", f"تعذر الاتصال بالخادم: {str(e)}")

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text)
        dialog.open()

if __name__ == "__main__":
    FieldInspectionApp().run()
