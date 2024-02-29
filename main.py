import sqlite3
from random import shuffle

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        self.conn = sqlite3.connect('numbers.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS numbers (value INTEGER)''')
        self.conn.commit()

        layout = BoxLayout(orientation='vertical')

        self.create_button = Button(text='Createbutton')
        self.create_button.bind(on_press=self.create_numbers)

        self.generate_button = Button(text='Generatebutton')
        self.generate_button.bind(on_press=self.generate_numbers)

        self.label = Label(text='TextLabel')

        self.scroll_input = TextInput(text='10', input_filter='int', multiline=False)
        self.scroll_input1 = TextInput(text='5', input_filter='int', multiline=False)

        layout.add_widget(self.create_button)
        layout.add_widget(self.scroll_input)
        layout.add_widget(self.label)
        layout.add_widget(self.generate_button)
        layout.add_widget(self.scroll_input1)

        return layout

    def create_numbers(self, instance):
        self.c.execute('DELETE FROM numbers')
        max_number = int(self.scroll_input.text)
        rand_numbers = list(range(1, max_number + 1))
        shuffle(rand_numbers)
        self.c.executemany('INSERT INTO numbers (value) VALUES (?)', [(num,) for num in rand_numbers])
        self.conn.commit()
        self.label.text = 'Created numbers in database.'

    def generate_numbers(self, instance):
        number_of_items = int(self.scroll_input1.text)
        self.c.execute('SELECT value FROM numbers LIMIT ?', (number_of_items,))
        fetched_numbers = self.c.fetchall()
        self.label.text = ', '.join(str(num[0]) for num in fetched_numbers)
        self.c.executemany('DELETE FROM numbers WHERE value = ?', fetched_numbers)
        self.conn.commit()

    def on_stop(self):
        self.conn.close()


if __name__ == '__main__':
    MyApp().run()
