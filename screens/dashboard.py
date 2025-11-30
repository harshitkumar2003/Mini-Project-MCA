import os
import sys
from os.path import dirname, abspath, join, exists
from datetime import datetime, timedelta
import random

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import (
    StringProperty, 
    ObjectProperty, 
    NumericProperty, 
    ListProperty
)
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp

# Add the project root directory to Python path
project_root = dirname(dirname(abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from data.health_data import DOCTORS, DISEASES


class InfoCard(BoxLayout):
    title = StringProperty('')
    value = StringProperty('')
    icon_source = StringProperty('')
    action = ObjectProperty(None)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.action:
            self.action()
            return True
        return super().on_touch_down(touch)


class DoctorCard(BoxLayout):
    name = StringProperty('')
    specialization = StringProperty('')
    available = StringProperty('')
    _image_source = StringProperty('')
    on_select = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set basic properties
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (200, 300)
        self.padding = 15
        self.spacing = 10
        
        # Create the UI elements
        self._create_ui()
        
        # Bind properties
        self.bind(
            name=self._update_ui,
            specialization=self._update_ui,
            available=self._update_ui,
            _image_source=self._update_image,
            pos=self._update_rect,
            size=self._update_rect
        )
    
    def _create_ui(self):
        """Create all UI elements for the doctor card."""
        from kivy.uix.image import Image
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.graphics import Color, RoundedRectangle, Line
        
        # Create image container
        img_container = BoxLayout(size_hint_y=0.4)
        
        # Create image widget
        self.img = Image(
            source='assets/doctor.png',
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        img_container.add_widget(self.img)
        
        # Create labels
        self.name_label = Label(
            text=self.name or 'Dr. Unknown',
            font_size=16,
            bold=True,
            size_hint_y=None,
            height=30,
            halign='center',
            valign='middle'
        )
        
        self.specialization_label = Label(
            text=self.specialization or 'General Physician',
            font_size=14,
            color=(0.3, 0.5, 0.3, 1),
            size_hint_y=None,
            height=25,
            halign='center',
            valign='middle'
        )
        
        self.available_label = Label(
            text=self.available or 'Contact for availability',
            font_size=12,
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=40,
            halign='center',
            valign='middle',
            text_size=(180, None),
            shorten=True,
            shorten_from='right'
        )
        
        # Create book button
        self.book_btn = Button(
            text='Book Appointment',
            size_hint=(0.8, None),
            height=40,
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.6, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.book_btn.bind(on_release=self.select_doctor)
        
        # Add all widgets to the layout
        self.add_widget(img_container)
        self.add_widget(self.name_label)
        self.add_widget(self.specialization_label)
        self.add_widget(self.available_label)
        # Add a simple BoxLayout as a spacer instead of Widget
        spacer = BoxLayout(size_hint_y=0.1)
        self.add_widget(spacer)
        self.add_widget(self.book_btn)
        
        # Draw the background and border
        with self.canvas.before:
            self.bg_color = Color(0.95, 0.97, 1, 1)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[10,])
            self.border_color = Color(0.2, 0.6, 0.4, 0.2)
            self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=1.5)
            
        # Update the image source after UI is created
        if hasattr(self, '_image_source') and self._image_source:
            self.img.source = self._image_source
    
    def _update_ui(self, *args):
        """Update the UI elements when properties change."""
        if hasattr(self, 'name_label'):
            self.name_label.text = self.name or 'Dr. Unknown'
        if hasattr(self, 'specialization_label'):
            self.specialization_label.text = self.specialization or 'General Physician'
        if hasattr(self, 'available_label'):
            self.available_label.text = self.available or 'Contact for availability'
    
    def _update_image(self, *args):
        """Update the doctor's image."""
        if not hasattr(self, 'img'):
            return
            
        if not self._image_source or not os.path.exists(self._image_source):
            self.img.source = 'assets/doctor.png'
        else:
            self.img.source = self._image_source
            
        # Force reload of the image
        self.img.reload()
    
    def _update_rect(self, *args):
        """Update the background and border when size or position changes."""
        if hasattr(self, 'rect') and hasattr(self, 'border'):
            self.rect.pos = self.pos
            self.rect.size = self.size
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, 10)
    
    def select_doctor(self, instance=None):
        """Handle doctor selection."""
        if self.on_select:
            self.on_select({
                'name': self.name,
                'specialization': self.specialization,
                'available': self.available
            })
    
    def select(self, *args):
        """Alias for select_doctor for KV language compatibility."""
        self.select_doctor()
    
    def on_name(self, instance, value):
        if hasattr(self, 'name_label'):
            self.name_label.text = value or 'Dr. Unknown'
    
    def on_specialization(self, instance, value):
        if hasattr(self, 'specialization_label'):
            self.specialization_label.text = value or 'General Physician'
    
    def on_available(self, instance, value):
        if hasattr(self, 'available_label'):
            self.available_label.text = value or 'Contact for availability'
    
    def on__image_source(self, instance, value):
        if not hasattr(self, 'img'):
            return
            
        if value and os.path.exists(value):
            self.img.source = value
        else:
            self.img.source = 'assets/doctor.png'
    
    def select_doctor(self, *args):
        if self.on_select:
            self.on_select({
                'name': self.name,
                'specialization': self.specialization,
                'available': self.available
            })
            try:
                self.on_select({
                    'name': self.name,
                    'specialization': self.specialization,
                    'available': self.available
                })
            except Exception as e:
                print(f"Error in select_doctor: {e}")
    
    # Alias for Kivy KV language compatibility
    def select(self, *args):
        self.select_doctor()

class DiseaseInfo(BoxLayout):
    name = StringProperty('')
    symptoms = StringProperty('')
    doctor = StringProperty('')
    medication = StringProperty('')
    advice = StringProperty('')


class AppointmentPopup(Popup):
    def __init__(self, doctor, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Book Appointment with {doctor['name']}"
        self.size_hint = (0.9, 0.8)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Doctor info
        layout.add_widget(Label(
            text=f"{doctor['name']}\n{doctor['specialization']}",
            size_hint_y=None,
            height=60,
            halign='center',
            font_size=18,
            bold=True
        ))
        
        # Date picker
        layout.add_widget(Label(text="Select Date:", size_hint_y=None, height=30))
        self.date_spinner = Spinner(
            text='Select Date',
            values=self._get_available_dates(doctor['available']),
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.date_spinner)
        
        # Time slot
        layout.add_widget(Label(text="Select Time Slot:", size_hint_y=None, height=30))
        self.time_spinner = Spinner(
            text='Select Time',
            values=['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM', '04:00 PM'],
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.time_spinner)
        
        # Reason for visit
        layout.add_widget(Label(text="Reason for Visit:", size_hint_y=None, height=30))
        self.reason_input = TextInput(
            multiline=True,
            size_hint_y=0.4,
            hint_text="Briefly describe your symptoms or reason for the appointment"
        )
        layout.add_widget(self.reason_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_cancel = Button(text='Cancel', on_press=self.dismiss)
        btn_confirm = Button(
            text='Confirm Appointment',
            background_color=get_color_from_hex('#4CAF50'),
            on_press=self.confirm_appointment
        )
        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_confirm)
        layout.add_widget(btn_layout)
        
        self.content = layout
    
    def _get_available_dates(self, available_days):
        # Generate dates for the next 14 days
        dates = []
        today = datetime.now()
        for i in range(1, 15):
            date = today + timedelta(days=i)
            if date.strftime('%a') in available_days:
                dates.append(date.strftime('%Y-%m-%d (%A)'))
        return dates or ['No available dates']
    
    def confirm_appointment(self, instance):
        # Here you would typically save the appointment to a database
        confirmation = f"Appointment confirmed!\n\n"
        confirmation += f"Doctor: {self.title}\n"
        confirmation += f"Date: {self.date_spinner.text}\n"
        confirmation += f"Time: {self.time_spinner.text}\n"
        confirmation += f"Reason: {self.reason_input.text}"
        
        popup = Popup(
            title='Appointment Confirmed',
            content=Label(text=confirmation, padding=20),
            size_hint=(0.8, 0.6)
        )
        popup.open()
        self.dismiss()

class SymptomTrackerPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Symptom Tracker"
        self.size_hint = (0.9, 0.9)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Symptom input
        layout.add_widget(Label(
            text="Enter your symptoms (comma separated):",
            size_hint_y=None,
            height=30
        ))
        
        self.symptom_input = TextInput(
            hint_text="e.g., headache, fever, cough",
            size_hint_y=None,
            height=100,
            multiline=True
        )
        layout.add_widget(self.symptom_input)
        
        # Analyze button
        btn_analyze = Button(
            text="Analyze Symptoms",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex('#2196F3'),
            on_press=self.analyze_symptoms
        )
        layout.add_widget(btn_analyze)
        
        # Results area
        self.results_layout = BoxLayout(orientation='vertical', spacing=5)
        scroll = ScrollView()
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)
        
        self.content = layout
    
    def analyze_symptoms(self, instance):
        symptoms = [s.strip().lower() for s in self.symptom_input.text.split(',') if s.strip()]
        if not symptoms:
            return
        
        self.results_layout.clear_widgets()
        
        # Find matching diseases
        matches = []
        for disease, data in DISEASES.items():
            disease_symptoms = [s.lower() for s in data['symptoms']]
            match_count = sum(1 for s in symptoms if any(s in ds or ds in s for ds in disease_symptoms))
            if match_count > 0:
                matches.append((disease, match_count / len(disease_symptoms)))
        
        # Sort by match percentage
        matches.sort(key=lambda x: x[1], reverse=True)
        
        if not matches:
            self.results_layout.add_widget(Label(
                text="No matching conditions found. Please consult a doctor.",
                color=(0.8, 0, 0, 1)
            ))
            return
        
        # Show top 3 matches
        self.results_layout.add_widget(Label(
            text="Possible Conditions:",
            size_hint_y=None,
            height=40,
            font_size=16,
            bold=True
        ))
        
        for disease, confidence in matches[:3]:
            disease_info = DISEASES[disease]
            disease_widget = DiseaseInfo(
                name=disease,
                symptoms=", ".join(disease_info['symptoms']),
                doctor=f"Recommended Specialist: {disease_info['doctor']}",
                medication="Medications: " + ", ".join(disease_info['medication']),
                advice=disease_info['advice']
            )
            self.results_layout.add_widget(disease_widget)
            
            # Add book appointment button for this specialist
            btn_book = Button(
                text=f"Book with {disease_info['doctor']}",
                size_hint_y=None,
                height=40,
                background_color=get_color_from_hex('#4CAF50'),
                on_press=lambda x, d=disease_info['doctor']: self.book_specialist(d)
            )
            self.results_layout.add_widget(btn_book)
    
    def book_specialist(self, specialist_type):
        # Find doctors matching the specialist type
        matching_doctors = [d for d in DOCTORS if specialist_type.lower() in d['specialization'].lower()]
        
        if not matching_doctors:
            # If no exact match, show all doctors
            matching_doctors = DOCTORS
        
        popup = Popup(
            title=f"Available {specialist_type}s",
            size_hint=(0.9, 0.8)
        )
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        scroll = ScrollView()
        doctors_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        doctors_layout.bind(minimum_height=doctors_layout.setter('height'))
        
        for doctor in matching_doctors:
            card = DoctorCard(
                name=doctor['name'],
                specialization=doctor['specialization'],
                available=f"Available: {', '.join(doctor['available'])}",
                _image_source=doctor.get('image', 'assets/doctor.png'),
                on_select=lambda d=doctor: self.show_appointment_popup(d)
            )
            doctors_layout.add_widget(card)
        
        scroll.add_widget(doctors_layout)
        layout.add_widget(scroll)
        
        btn_close = Button(
            text="Close",
            size_hint_y=None,
            height=50,
            on_press=popup.dismiss
        )
        layout.add_widget(btn_close)
        
        popup.content = layout
        popup.open()
    
    def show_appointment_popup(self, doctor):
        popup = AppointmentPopup(doctor=doctor)
        popup.open()

class HomeDashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appointments = []
        self.saved_reports = []
        self.diseases = []  # Initialize empty diseases list
        self.diseases = list(DISEASES.keys())  # Load diseases from health_data
        
    def on_enter(self, *args):
        # Initialize health graph
        self.init_health_graph()
        
        # Update info cards
        self.update_info_cards()
        
        # Load doctors
        self.load_doctors()
        
        # Update diseases count in the UI
        if hasattr(self, 'ids') and 'diseases_card' in self.ids:
            self.ids.diseases_card.value = str(len(self.diseases))
    
    def init_health_graph(self):
        """Initialize the health graph with sample data using Canvas drawing"""
        graph = self.ids.health_graph
        
        # Clear any existing drawings
        graph.canvas.after.clear()
        
        # Get graph dimensions
        width, height = graph.size
        padding = dp(20)
        
        # Draw grid lines
        with graph.canvas.after:
            # Grid color
            Color(0.9, 0.9, 0.9, 1)
            
            # Vertical grid lines
            for i in range(6):
                x = padding + (width - 2 * padding) * i / 5
                Line(points=[x, padding, x, height - padding], width=0.5)
            
            # Horizontal grid lines
            for i in range(6):
                y = padding + (height - 2 * padding) * i / 5
                Line(points=[padding, y, width - padding, y], width=0.5)
            
            # Graph border
            Color(0.7, 0.7, 0.7, 1)
            Line(rectangle=(padding, padding, 
                          width - 2 * padding, 
                          height - 2 * padding), 
                width=1)
            
            # Sample data points (x, y)
            points = [(i, random.randint(50, 100)) for i in range(30)]
            
            # Scale points to fit the graph
            scaled_points = []
            x_scale = (width - 2 * padding) / 30.0
            y_scale = (height - 2 * padding) / 100.0
            
            for x, y in points:
                px = padding + x * x_scale
                py = padding + y * y_scale
                scaled_points.extend([px, py])
            
            # Draw the line
            Color(0.3, 0.7, 0.3, 1)  # Green color
            Line(points=scaled_points, width=2)
    
    def update_info_cards(self):
        # Update all info cards with sample data
        cards_data = {
            'appointments_card': str(len(self.appointments)),
            'reports_card': str(len(self.saved_reports)),
            'doctors_card': str(len(DOCTORS)),
            'symptoms_card': 'Track',
            'medicines_card': '15',
            'diseases_card': str(len(DISEASES))
        }
        
        for card_id, value in cards_data.items():
            if hasattr(self.ids, card_id):
                self.ids[card_id].value = value
    
    def load_doctors(self):
        try:
            # Clear existing doctor cards
            container = self.ids.doctors_container
            container.clear_widgets()
            
            # Add doctor cards
            for doctor in DOCTORS:
                try:
                    # Create a new DoctorCard instance with properties
                    card = DoctorCard(
                        name=doctor.get('name', 'Dr. Unknown'),
                        specialization=doctor.get('specialization', 'General Physician'),
                        available=f"Available: {', '.join(doctor.get('available', ['Contact for availability']))}",
                        _image_source=doctor.get('image', 'assets/doctor.png')
                    )
                    card.on_select = lambda d=doctor: self.show_appointment_popup(d)
                    container.add_widget(card)
                except Exception as e:
                    print(f"Error creating doctor card: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # Update doctors count in the UI
            if hasattr(self, 'ids') and 'doctors_card' in self.ids:
                self.ids.doctors_card.value = str(len(DOCTORS))
                
        except Exception as e:
            print(f"Error in load_doctors: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def show_appointment_popup(self, doctor):
        popup = AppointmentPopup(doctor=doctor)
        popup.open()
    
    def show_symptom_tracker(self):
        popup = SymptomTrackerPopup()
        popup.open()
    
    def show_doctor_list(self, *args):
        try:
            # This method is called when the doctors card is clicked
            popup = Popup(
                title='Our Doctors',
                size_hint=(0.9, 0.8)
            )
            
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            scroll = ScrollView()
            doctors_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            doctors_layout.bind(minimum_height=doctors_layout.setter('height'))
            
            for doctor in DOCTORS:
                try:
                    # Create a new DoctorCard instance with properties
                    card = DoctorCard(
                        name=doctor.get('name', 'Dr. Unknown'),
                        specialization=doctor.get('specialization', 'General Physician'),
                        available=f"Available: {', '.join(doctor.get('available', ['Contact for availability']))}",
                        _image_source=doctor.get('image', 'assets/doctor.png')
                    )
                    card.on_select = lambda d=doctor: self.show_appointment_popup(d)
                    doctors_layout.add_widget(card)
                except Exception as e:
                    print(f"Error creating doctor card in popup: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            scroll.add_widget(doctors_layout)
            layout.add_widget(scroll)
            
            close_btn = Button(
                text='Close',
                size_hint=(1, 0.1),
                background_color=(0.8, 0.2, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            close_btn.bind(on_release=popup.dismiss)
            layout.add_widget(close_btn)
            
            popup.content = layout
            popup.open()
            
        except Exception as e:
            print(f"Error in show_doctor_list: {str(e)}")
            import traceback
            traceback.print_exc()
