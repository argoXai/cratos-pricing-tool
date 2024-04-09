import io
import threading
import asyncio
import traceback
from functools import partial

import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image

from CLEAN_MC import main_func


# Appearance Mode
ctk.set_appearance_mode('system')  # default
# ctk.set_appearance_mode('dark')
# ctk.set_appearance_mode('light')

# Color theme
# ctk.set_default_color_theme('blue')  # default
# ctk.set_default_color_theme('dark-blue')
ctk.set_default_color_theme('green')


class FormFrame(ctk.CTkFrame):
    def __init__(self, master, form_data, **kwargs):
        super().__init__(master, **kwargs)
        
        # Custom validation function to allow only numeric input
        def numbers_validation(value):
            if value.isdigit():
                return True
            else:
                return False
        numbers_validation = self.register(numbers_validation)


        # Custom validation function to allow only float
        def float_validation(value):
            # validate letters
            if any(v.isalpha() for v in value):
                return False
            
            elif any(v.isspace() for v in value):
                return False
            
            # validate if can be float
            try:
                float(value)
                return True
            except ValueError:
                return False
        float_validation = self.register(float_validation)


        # slider event handler for int values
        def slider_event_int(value, var_name):
            int_value = int(value)
            var = getattr(master, var_name)
            var.set(int_value)
            form_data[var_name] = int_value


        # slider event handler for str -> float values
        def slider_event_float(value, var_name, round_value=2):
            float_value = round(float(value), round_value)
            var = getattr(master, var_name)
            var.set(float_value)
            form_data[var_name] = float_value


        # input event handler
        def input_event(instance, slider, param_name):
            def handler(event):
                value = instance.get()

                if type(value) == int:
                    slider.set(int(value))
                    master.form_data[param_name] = int(value)

                if type(value) == str:
                    slider.set(float(value))
                    master.form_data[param_name] = float(value)

            return handler
        
        # input event handler
        def input_event_int(instance, slider, param_name):
            def handler(event):
                value = instance.get()

                try:
                    int_value = int(value)
                    slider.set(int(value))
                    master.form_data[param_name] = int(value)
                except ValueError:
                    print('INCORRECT VALUE!: ', instance, value)
                    pass
            return handler


        row = 0

        # ------ Title of frame ------ #
        title = ctk.CTkLabel(master=self, text='Calculation params:', font=('Arial', 16, 'bold'))
        title.grid(row=row, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

        row += 1

        # ------ Number of Simulations ------ #
        label1 = ctk.CTkLabel(master=self, text='Number of Simulations:\n' + str('(def: '+str(master.defaults['num_simulations'])+')'), font=('Arial', 14, 'bold'))
        label1.grid(row=row, column=0, padx=10, pady=10)

        input1 = ctk.CTkEntry(
            master=self, textvariable=master.num_simulations,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input1.grid(row=row, column=1, padx=10, pady=10)

        slider1 = ctk.CTkSlider(self, from_=1, to=(int(master.num_simulations.get()) * 2),
                                command=lambda value: slider_event_int(value, 'num_simulations'))
        slider1.configure(number_of_steps=(int(master.num_simulations.get()) * 2 * 1000))
        slider1.set(int(master.num_simulations.get()))
        slider1.grid(row=row, column=2, padx=10, pady=10)

        input1.bind('<KeyRelease>', input_event_int(input1, slider1, 'num_simulations'))

        row += 1

        divider_5 = tk.Label(master=self)
        divider_5.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1

        # ------ notice_pct_dist labels ------ #        
        label2_0 = ctk.CTkLabel(master=self, text='notice_pct_dist:', font=('Arial', 14, 'bold'))
        label2_0.grid(row=row, column=0, padx=10, pady=10, columnspan=4)

        row += 1

        label2_1 = ctk.CTkLabel(master=self, text='x1:\n' + str('(def: '+str(master.defaults['notice_pct_dist_x1'])+')'))
        label2_1.grid(row=row, column=0, padx=0, pady=0)

        label2_2 = ctk.CTkLabel(master=self, text='x2:\n' + str('(def: '+str(master.defaults['notice_pct_dist_x2'])+')'))
        label2_2.grid(row=row, column=1, padx=0, pady=0)

        label2_3 = ctk.CTkLabel(master=self, text='x3:\n' + str('(def: '+str(master.defaults['notice_pct_dist_x3'])+')'))
        label2_3.grid(row=row, column=2, padx=0, pady=0)

        label2_4 = ctk.CTkLabel(master=self, text='x4:\n' + str('(def: '+str(master.defaults['notice_pct_dist_x4'])+')'))
        label2_4.grid(row=row, column=3, padx=0, pady=0)

        row += 1

        # ------ notice_pct_dist inputs ------ #
        # notice_pct_dist_x1
        input2_1 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_dist_x1,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input2_1.grid(row=row, column=0, padx=10, pady=0)

        # notice_pct_dist_x2
        input2_2 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_dist_x2,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input2_2.grid(row=row, column=1, padx=10, pady=0)

        # notice_pct_dist_x3
        input2_3 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_dist_x3,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input2_3.grid(row=row, column=2, padx=10, pady=0)

        # notice_pct_dist_x4
        input2_4 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_dist_x4,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input2_4.grid(row=row, column=3, padx=10, pady=0)

        row += 1

        slider2_1 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_dist_x1'))
        slider2_1.configure(number_of_steps=1000)
        slider2_1.set(float(master.notice_pct_dist_x1.get()))
        slider2_1.grid(row=row, column=0, padx=20, pady=10)

        input2_1.bind('<KeyRelease>', input_event(input2_1, slider2_1, 'notice_pct_dist_x1'))

        slider2_2 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_dist_x2'))
        slider2_2.configure(number_of_steps=1000)
        slider2_2.set(float(master.notice_pct_dist_x2.get()))
        slider2_2.grid(row=row, column=1, padx=20, pady=10)

        input2_2.bind('<KeyRelease>', input_event(input2_2, slider2_2, 'notice_pct_dist_x2'))

        slider2_3 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_dist_x3'))
        slider2_3.configure(number_of_steps=1000)
        slider2_3.set(float(master.notice_pct_dist_x3.get()))
        slider2_3.grid(row=row, column=2, padx=20, pady=10)

        input2_3.bind('<KeyRelease>', input_event(input2_3, slider2_3, 'notice_pct_dist_x3'))

        slider2_4 = ctk.CTkSlider(self, from_=0, to=(int(master.notice_pct_dist_x4.get())*2), command=lambda value: slider_event_int(value, 'notice_pct_dist_x4'))
        slider2_4.configure(number_of_steps=(int(master.notice_pct_dist_x4.get())*2*10000))
        slider2_4.set(float(master.notice_pct_dist_x4.get()))
        slider2_4.grid(row=row, column=3, padx=20, pady=10)

        input2_4.bind('<KeyRelease>', input_event(input2_4, slider2_4, 'notice_pct_dist_x4'))

        row += 1

        divider_4 = tk.Label(master=self)
        divider_4.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1

        # ------ notice_pct_loss_dist labels ------ #
        label3_0 = ctk.CTkLabel(master=self, text='notice_pct_loss_dist:', font=('Arial', 14, 'bold'))
        label3_0.grid(row=row, column=0, padx=10, pady=10, columnspan=4)

        row += 1
        label3_1 = ctk.CTkLabel(master=self, text='x1:\n' + str('(def: '+str(master.defaults['notice_pct_loss_dist_x1'])+')'))
        label3_1.grid(row=row, column=0, padx=0, pady=0)

        label3_2 = ctk.CTkLabel(master=self, text='x2:\n' + str('(def: '+str(master.defaults['notice_pct_loss_dist_x2'])+')'))
        label3_2.grid(row=row, column=1, padx=0, pady=0)

        label3_3 = ctk.CTkLabel(master=self, text='x3:\n' + str('(def: '+str(master.defaults['notice_pct_loss_dist_x3'])+')'))
        label3_3.grid(row=row, column=2, padx=0, pady=0)

        label3_4 = ctk.CTkLabel(master=self, text='x4:\n' + str('(def: '+str(master.defaults['notice_pct_loss_dist_x4'])+')'))
        label3_4.grid(row=row, column=3, padx=0, pady=0)

        row += 1

        # ------ notice_pct_loss_dist inputs ------ #
        # notice_pct_loss_dist_x1
        input3_1 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_loss_dist_x1,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_1.grid(row=row, column=0, padx=10, pady=0)

        # notice_pct_loss_dist_x2
        input3_2 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_loss_dist_x2,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_2.grid(row=row, column=1, padx=10, pady=0)

        # notice_pct_loss_dist_x3
        input3_3 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_loss_dist_x3,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_3.grid(row=row, column=2, padx=10, pady=0)

        # notice_pct_loss_dist_x4
        input3_4 = ctk.CTkEntry(
            master=self, textvariable=master.notice_pct_loss_dist_x4,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input3_4.grid(row=row, column=3, padx=10, pady=0)

        row += 1

        slider3_1 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_loss_dist_x1'))
        slider3_1.configure(number_of_steps=1000)
        slider3_1.set(float(master.notice_pct_loss_dist_x1.get()))
        slider3_1.grid(row=row, column=0, padx=20, pady=10)

        input3_1.bind('<KeyRelease>', input_event(input3_1, slider3_1, 'notice_pct_loss_dist_x1'))

        slider3_2 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_loss_dist_x2'))
        slider3_2.configure(number_of_steps=1000)
        slider3_2.set(float(master.notice_pct_loss_dist_x2.get()))
        slider3_2.grid(row=row, column=1, padx=20, pady=10)

        input3_2.bind('<KeyRelease>', input_event(input3_2, slider3_2, 'notice_pct_loss_dist_x2'))

        slider3_3 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'notice_pct_loss_dist_x3'))
        slider3_3.configure(number_of_steps=1000)
        slider3_3.set(float(master.notice_pct_loss_dist_x3.get()))
        slider3_3.grid(row=row, column=2, padx=20, pady=10)

        input3_3.bind('<KeyRelease>', input_event(input3_3, slider3_3, 'notice_pct_loss_dist_x3'))

        slider3_4 = ctk.CTkSlider(self, from_=1, to=(int(master.notice_pct_loss_dist_x4.get())*2), command=lambda value: slider_event_int(value, 'notice_pct_loss_dist_x4'))
        slider3_4.configure(number_of_steps=(int(master.notice_pct_loss_dist_x4.get())*2*10000))
        slider3_4.set(float(master.notice_pct_loss_dist_x4.get()))
        slider3_4.grid(row=row, column=3, padx=20, pady=10)

        input3_4.bind('<KeyRelease>', input_event(input3_4, slider3_4, 'notice_pct_loss_dist_x4'))

        row += 1

        divider_2 = tk.Label(master=self)
        divider_2.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1

        # ------ severity_dist labels ------ #
        label4_0 = ctk.CTkLabel(master=self, text='severity_dist:', font=('Arial', 14, 'bold'))
        label4_0.grid(row=row, column=0, padx=10, pady=10, columnspan=4)

        row += 1

        label4_1 = ctk.CTkLabel(master=self, text='x1:\n' + str('(def: '+str(master.defaults['severity_dist_x1'])+')'))
        label4_1.grid(row=row, column=0, padx=0, pady=0)

        label4_2 = ctk.CTkLabel(master=self, text='x2:\n' + str('(def: '+str(master.defaults['severity_dist_x2'])+')'))
        label4_2.grid(row=row, column=1, padx=0, pady=0)

        label4_3 = ctk.CTkLabel(master=self, text='x3:\n' + str('(def: '+str(master.defaults['severity_dist_x3'])+')'))
        label4_3.grid(row=row, column=2, padx=0, pady=0)

        label4_4 = ctk.CTkLabel(master=self, text='x4:\n' + str('(def: '+str(master.defaults['severity_dist_x4'])+')'))
        label4_4.grid(row=row, column=3, padx=0, pady=0)

        row += 1

        # ------ severity_dist inputs ------ #
        # severity_dist_x1
        input3_1_1 = ctk.CTkEntry(
            master=self, textvariable=master.severity_dist_x1,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_1_1.grid(row=row, column=0, padx=10, pady=0)

        # severity_dist_x2
        input3_2_1 = ctk.CTkEntry(
            master=self, textvariable=master.severity_dist_x2,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_2_1.grid(row=row, column=1, padx=10, pady=0)

        # severity_dist_x3
        input3_3_1 = ctk.CTkEntry(
            master=self, textvariable=master.severity_dist_x3,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input3_3_1.grid(row=row, column=2, padx=10, pady=0)

        # severity_dist_x4
        input3_4_1 = ctk.CTkEntry(
            master=self, textvariable=master.severity_dist_x4,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input3_4_1.grid(row=row, column=3, padx=10, pady=0)

        row += 1

        slider3_1_1 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'severity_dist_x1'))
        slider3_1_1.configure(number_of_steps=1000)
        slider3_1_1.set(float(master.severity_dist_x1.get()))
        slider3_1_1.grid(row=row, column=0, padx=20, pady=10)

        input3_1_1.bind('<KeyRelease>', input_event(input3_1_1, slider3_1_1, 'severity_dist_x1'))

        slider3_2_1 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'severity_dist_x2'))
        slider3_2_1.configure(number_of_steps=1000)
        slider3_2_1.set(float(master.severity_dist_x2.get()))
        slider3_2_1.grid(row=row, column=1, padx=20, pady=10)

        input3_2_1.bind('<KeyRelease>', input_event(input3_2_1, slider3_2_1, 'severity_dist_x2'))

        slider3_3_1 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'severity_dist_x3'))
        slider3_3_1.configure(number_of_steps=1000)
        slider3_3_1.set(float(master.severity_dist_x3.get()))
        slider3_3_1.grid(row=row, column=2, padx=20, pady=10)

        input3_3_1.bind('<KeyRelease>', input_event(input3_3_1, slider3_3_1, 'severity_dist_x3'))

        slider3_4_1 = ctk.CTkSlider(self, from_=1, to=(int(master.severity_dist_x4.get())*2), command=lambda value: slider_event_int(value, 'severity_dist_x4'))
        slider3_4_1.configure(number_of_steps=(int(master.severity_dist_x4.get())*2*10000))
        slider3_4_1.set(float(master.severity_dist_x4.get()))
        slider3_4_1.grid(row=row, column=3, padx=20, pady=10)

        input3_4_1.bind('<KeyRelease>', input_event(input3_4_1, slider3_4_1, 'severity_dist_x4'))

        row += 1

        divider_3 = tk.Label(master=self)
        divider_3.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1

        # ------ deal_count ------ #
        label3 = ctk.CTkLabel(master=self, text='deal_count:\n' + str('(def: '+str(master.defaults['deal_count'])+')'), font=('Arial', 14, 'bold'))
        label3.grid(row=row, column=0, padx=10, pady=20)

        input3 = ctk.CTkEntry(
            master=self, textvariable=master.deal_count,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input3.grid(row=row, column=1, padx=10, pady=20)

        slider4 = ctk.CTkSlider(self, from_=0, to=(int(master.deal_count.get())*2), command=lambda value: slider_event_int(value, 'deal_count'))
        slider4.configure(number_of_steps=(int(master.deal_count.get())*2*10000))
        slider4.set(float(master.deal_count.get()))
        slider4.grid(row=row, column=2, padx=20, pady=10)

        input3.bind('<KeyRelease>', input_event(input3, slider4, 'deal_count'))


        row += 1

        # ------ DV_range ------ #
        label4 = ctk.CTkLabel(master=self, text='DV_range:\n' + str('(def: '+str(master.defaults['DV_range'])+')'), font=('Arial', 14, 'bold'))
        label4.grid(row=row, column=0, padx=10, pady=20)

        input4 = ctk.CTkEntry(
            master=self, textvariable=master.DV_range,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input4.grid(row=row, column=1, padx=10, pady=20)

        slider5 = ctk.CTkSlider(self, from_=0, to=(int(master.DV_range.get())*2), command=lambda value: slider_event_int(value, 'DV_range'))
        slider5.configure(number_of_steps=(int(master.DV_range.get())*2*10000))
        slider5.set(float(master.DV_range.get()))
        slider5.grid(row=row, column=2, padx=20, pady=0)

        input4.bind('<KeyRelease>', input_event(input4, slider5, 'deal_count'))

        row += 1

        divider_6 = tk.Label(master=self)
        divider_6.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1

        # ------ sme_low_DV ------ #
        label5 = ctk.CTkLabel(master=self, text='sme_low_DV:\n' + str('(def: '+str(master.defaults['sme_low_DV'])+')'), font=('Arial', 14, 'bold'))
        label5.grid(row=row, column=0, padx=10, pady=20)

        input5 = ctk.CTkEntry(
            master=self, textvariable=master.sme_low_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input5.grid(row=row, column=1, padx=10, pady=20)



        # ------ sme_upper_DV ------ #
        label6 = ctk.CTkLabel(master=self, text='sme_upper_DV:\n' + str('(def: '+str(master.defaults['sme_upper_DV'])+')'), font=('Arial', 14, 'bold'))
        label6.grid(row=row, column=2, padx=10, pady=20)

        input6 = ctk.CTkEntry(
            master=self, textvariable=master.sme_upper_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input6.grid(row=row, column=3, padx=10, pady=20)

        row += 1

        slider6 = ctk.CTkSlider(self, from_=0, to=(int(master.sme_low_DV.get())*2), command=lambda value: slider_event_int(value, 'sme_low_DV'))
        slider6.configure(number_of_steps=(int(master.sme_low_DV.get())*2*10000))
        slider6.set(int(master.sme_low_DV.get()))
        slider6.grid(row=row, column=1, padx=20, pady=0)

        input5.bind('<KeyRelease>', input_event(input5, slider6, 'sme_low_DV'))


        slider7 = ctk.CTkSlider(self, from_=0, to=(int(master.sme_upper_DV.get())*2), command=lambda value: slider_event_int(value, 'sme_upper_DV'))
        slider7.configure(number_of_steps=(int(master.sme_upper_DV.get())*2*10000))
        slider7.set(int(master.sme_upper_DV.get()))
        slider7.grid(row=row, column=3, padx=20, pady=0)

        input6.bind('<KeyRelease>', input_event(input6, slider7, 'sme_upper_DV'))

        row += 1
        
        # ------ mm_low_DV ------ #
        label7 = ctk.CTkLabel(master=self, text='mm_low_DV:\n' + str('(def: '+str(master.defaults['mm_low_DV'])+')'), font=('Arial', 14, 'bold'))
        label7.grid(row=row, column=0, padx=10, pady=20)

        input7 = ctk.CTkEntry(
            master=self, textvariable=master.mm_low_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input7.grid(row=row, column=1, padx=10, pady=20)


        
        # ------ mm_upper_DV ------ #
        label8 = ctk.CTkLabel(master=self, text='mm_upper_DV:\n' + str('(def: '+str(master.defaults['mm_upper_DV'])+')'), font=('Arial', 14, 'bold'))
        label8.grid(row=row, column=2, padx=10, pady=20)

        input8 = ctk.CTkEntry(
            master=self, textvariable=master.mm_upper_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input8.grid(row=row, column=3, padx=10, pady=20)

        row += 1

        slider8_1 = ctk.CTkSlider(self, from_=0, to=(int(master.mm_low_DV.get())*2), command=lambda value: slider_event_int(value, 'mm_low_DV'))
        slider8_1.configure(number_of_steps=(int(master.mm_low_DV.get())*2*10000))
        slider8_1.set(int(master.mm_low_DV.get()))
        slider8_1.grid(row=row, column=1, padx=20, pady=0)

        slider8_2 = ctk.CTkSlider(self, from_=0, to=(int(master.mm_upper_DV.get())*2), command=lambda value: slider_event_int(value, 'mm_upper_DV'))
        slider8_2.configure(number_of_steps=(int(master.mm_upper_DV.get())*2*10000))
        slider8_2.set(int(master.mm_upper_DV.get()))
        slider8_2.grid(row=row, column=3, padx=20, pady=0)

        input7.bind('<KeyRelease>', input_event(input7, slider8_1, 'mm_low_DV'))
        input8.bind('<KeyRelease>', input_event(input8, slider8_2, 'mm_upper_DV'))

        row += 1

        divider_1 = tk.Label(master=self)
        divider_1.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1
        
        # ------ sme_pct ------ #
        label9 = ctk.CTkLabel(master=self, text='sme_pct:\n' + str('(def: '+str(master.defaults['sme_pct'])+')'), font=('Arial', 14, 'bold'))
        label9.grid(row=row, column=0, padx=10, pady=20)

        input9 = ctk.CTkEntry(
            master=self, textvariable=master.sme_pct,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input9.grid(row=row, column=1, padx=10, pady=20)

        slider9 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'sme_pct'))
        slider9.configure(number_of_steps=1000)
        slider9.set(float(master.sme_pct.get()))
        slider9.grid(row=row, column=2, padx=20, pady=10)

        input9.bind('<KeyRelease>', input_event(input9, slider9, 'sme_pct'))

        row += 1
        
        # ------ mm_pct ------ #
        label10 = ctk.CTkLabel(master=self, text='mm_pct:\n' + str('(def: '+str(master.defaults['mm_pct'])+')'), font=('Arial', 14, 'bold'))
        label10.grid(row=row, column=0, padx=10, pady=20)

        input10 = ctk.CTkEntry(
            master=self, textvariable=master.mm_pct,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input10.grid(row=row, column=1, padx=10, pady=20)

        slider10 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'mm_pct'))
        slider10.configure(number_of_steps=1000)
        slider10.set(float(master.mm_pct.get()))
        slider10.grid(row=row, column=2, padx=20, pady=10)

        input10.bind('<KeyRelease>', input_event(input10, slider10, 'mm_pct'))

        row += 1

        divider_7 = tk.Label(master=self)
        divider_7.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)

        row += 1
        
        # ------ j_pct ------ #
        label11 = ctk.CTkLabel(master=self, text='j_pct:\n' + str('(def: '+str(master.defaults['j_pct'])+')'), font=('Arial', 14, 'bold'))
        label11.grid(row=row, column=0, padx=10, pady=20)

        input11 = ctk.CTkEntry(
            master=self, textvariable=master.j_pct,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input11.grid(row=row, column=1, padx=10, pady=20)

        slider11 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'j_pct'))
        slider11.configure(number_of_steps=1000)
        slider11.set(float(master.j_pct.get()))
        slider11.grid(row=row, column=2, padx=20, pady=10)

        input11.bind('<KeyRelease>', input_event(input11, slider11, 'j_pct'))

        row += 1

        # ------ j_low_DV ------ #
        label12 = ctk.CTkLabel(master=self, text='j_low_DV:\n' + str('(def: '+str(master.defaults['j_low_DV'])+')'), font=('Arial', 14, 'bold'))
        label12.grid(row=row, column=0, padx=10, pady=20)

        input12 = ctk.CTkEntry(
            master=self, textvariable=master.j_low_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input12.grid(row=row, column=1, padx=10, pady=20)


        # ------ j_upper_DV ------ #
        label13 = ctk.CTkLabel(master=self, text='j_upper_DV:\n' + str('(def: '+str(master.defaults['j_upper_DV'])+')'), font=('Arial', 14, 'bold'))
        label13.grid(row=row, column=2, padx=10, pady=20)

        input13 = ctk.CTkEntry(
            master=self, textvariable=master.j_upper_DV,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input13.grid(row=row, column=3, padx=10, pady=20)
        
        row += 1

        slider12 = ctk.CTkSlider(self, from_=0, to=(int(master.j_low_DV.get())*2), command=lambda value: slider_event_int(value, 'j_low_DV'))
        slider12.configure(number_of_steps=(int(master.j_low_DV.get())*2*100000))
        slider12.set(int(master.j_low_DV.get()))
        slider12.grid(row=row, column=1, padx=20, pady=0)

        slider13 = ctk.CTkSlider(self, from_=0, to=(int(master.j_upper_DV.get())*2), command=lambda value: slider_event_int(value, 'j_upper_DV'))
        slider13.configure(number_of_steps=(int(master.j_upper_DV.get())*2*100000))
        slider13.set(int(master.j_upper_DV.get()))
        slider13.grid(row=row, column=3, padx=20, pady=0)

        input12.bind('<KeyRelease>', input_event(input12, slider12, 'j_low_DV'))
        input13.bind('<KeyRelease>', input_event(input13, slider13, 'j_upper_DV'))

        row += 1

        divider_8 = tk.Label(master=self)
        divider_8.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1

        label14_0 = ctk.CTkLabel(master=self, text='Limits:', font=('Arial', 14, 'bold'))
        label14_0.grid(row=row, column=0, padx=10, pady=10, columnspan=4)

        row += 1
        
        # ------ limits ------ #
        label14 = ctk.CTkLabel(master=self, text='low_limit:\n' + str('(def: '+str(master.defaults['low_limit'])+')'), font=('Arial', 14, 'bold'))
        label14.grid(row=row, column=0, padx=10)

        label15 = ctk.CTkLabel(master=self, text='upper_limit:\n' + str('(def: '+str(master.defaults['upper_limit'])+')'), font=('Arial', 14, 'bold'))
        label15.grid(row=row, column=1, padx=10)

        label16 = ctk.CTkLabel(master=self, text='limit_range:\n' + str('(def: '+str(master.defaults['limit_range'])+')'), font=('Arial', 14, 'bold'))
        label16.grid(row=row, column=2, padx=10)

        row += 1

        input14 = ctk.CTkEntry(
            master=self, textvariable=master.low_limit,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input14.grid(row=row, column=0, padx=10, pady=20)

        input15 = ctk.CTkEntry(
            master=self, textvariable=master.upper_limit,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input15.grid(row=row, column=1, padx=10, pady=20)


        input16 = ctk.CTkEntry(
            master=self, textvariable=master.limit_range,
            validate='key', validatecommand=(numbers_validation, '%P')
        )
        input16.grid(row=row, column=2, padx=10, pady=20)

        row += 1

        slider14 = ctk.CTkSlider(self, from_=0, to=(int(master.low_limit.get())*2), command=lambda value: slider_event_int(value, 'low_limit'))
        slider14.configure(number_of_steps=(int(master.low_limit.get())*2*100000))
        slider14.set(int(master.low_limit.get()))
        slider14.grid(row=row, column=0, padx=20, pady=0)


        slider15 = ctk.CTkSlider(self, from_=0, to=(int(master.upper_limit.get())*2), command=lambda value: slider_event_int(value, 'upper_limit'))
        slider15.configure(number_of_steps=(int(master.upper_limit.get())*2*100000))
        slider15.set(int(master.upper_limit.get()))
        slider15.grid(row=row, column=1, padx=20, pady=0)


        slider16 = ctk.CTkSlider(self, from_=0, to=(int(master.limit_range.get())*2), command=lambda value: slider_event_int(value, 'limit_range'))
        slider16.configure(number_of_steps=(int(master.limit_range.get())*2*100000))
        slider16.set(int(master.limit_range.get()))
        slider16.grid(row=row, column=2, padx=20, pady=0)

        input14.bind('<KeyRelease>', input_event(input14, slider14, 'low_limit'))
        input15.bind('<KeyRelease>', input_event(input15, slider15, 'upper_limit'))
        input16.bind('<KeyRelease>', input_event(input16, slider16, 'limit_range'))

        row += 1
        
        divider_9 = tk.Label(master=self)
        divider_9.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1

        # ------ primary_pct ------ #
        label17 = ctk.CTkLabel(master=self, text='primary_pct:\n' + str('(def: '+str(master.defaults['primary_pct'])+')'), font=('Arial', 14, 'bold'))
        label17.grid(row=row, column=0, padx=10)

        input17 = ctk.CTkEntry(
            master=self, textvariable=master.primary_pct,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input17.grid(row=row, column=1, padx=10, pady=20)

        
        # ------ xs_pct ------ #
        label18 = ctk.CTkLabel(master=self, text='xs_pct:\n' + str('(def: '+str(master.defaults['xs_pct'])+')'), font=('Arial', 14, 'bold'))
        label18.grid(row=row, column=2, padx=10)

        input18 = ctk.CTkEntry(
            master=self, textvariable=master.xs_pct,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input18.grid(row=row, column=3, padx=10, pady=20)
        
        row += 1

        slider17 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'primary_pct'))
        slider17.configure(number_of_steps=1000)
        slider17.set(float(master.primary_pct.get()))
        slider17.grid(row=row, column=1, padx=20, pady=10)


        slider18 = ctk.CTkSlider(self, from_=0.01, to=0.99, command=lambda value: slider_event_float(value, 'xs_pct'))
        slider18.configure(number_of_steps=1000)
        slider18.set(float(master.xs_pct.get()))
        slider18.grid(row=row, column=3, padx=20, pady=10)

        input17.bind('<KeyRelease>', input_event(input17, slider17, 'primary_pct'))

        input18.bind('<KeyRelease>', input_event(input18, slider18, 'xs_pct'))


        row += 1


        divider_10 = tk.Label(master=self)
        divider_10.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1

        # ------ pri_attachment_pt_range ------ #
        label19_0 = ctk.CTkLabel(master=self, text='pri_attachment_pt_range:', font=('Arial', 14, 'bold'))
        label19_0.grid(row=row, column=0, padx=10, pady=10, columnspan=4)

        row += 1
        
        
        label19_1 = ctk.CTkLabel(master=self, text='x1:\n' + str('(def: '+str(master.defaults['pri_attachment_pt_range_x1'])+')'), font=('Arial', 14, 'bold'))
        label19_1.grid(row=row, column=0, padx=10)

        label19_2 = ctk.CTkLabel(master=self, text='x2:\n' + str('(def: '+str(master.defaults['pri_attachment_pt_range_x2'])+')'), font=('Arial', 14, 'bold'))
        label19_2.grid(row=row, column=1, padx=10)

        label19_3 = ctk.CTkLabel(master=self, text='x3:\n' + str('(def: '+str(master.defaults['pri_attachment_pt_range_x3'])+')'), font=('Arial', 14, 'bold'))
        label19_3.grid(row=row, column=2, padx=10)

        row += 1

        input19_1 = ctk.CTkEntry(
            master=self, textvariable=master.pri_attachment_pt_range_x1,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input19_1.grid(row=row, column=0, padx=10, pady=20)

        input19_2 = ctk.CTkEntry(
            master=self, textvariable=master.pri_attachment_pt_range_x2,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input19_2.grid(row=row, column=1, padx=10, pady=20)

        input19_3 = ctk.CTkEntry(
            master=self, textvariable=master.pri_attachment_pt_range_x3,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input19_3.grid(row=row, column=2, padx=10, pady=20)

        row += 1

        slider20 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'pri_attachment_pt_range_x1', 5))
        slider20.configure(number_of_steps=1000000000)
        slider20.set(float(master.pri_attachment_pt_range_x1.get()))
        slider20.grid(row=row, column=0, padx=20, pady=10)

        slider21 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'pri_attachment_pt_range_x2', 5))
        slider21.configure(number_of_steps=1000000000)
        slider21.set(float(master.pri_attachment_pt_range_x2.get()))
        slider21.grid(row=row, column=1, padx=20, pady=10)

        slider22 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'pri_attachment_pt_range_x3', 5))
        slider22.configure(number_of_steps=1000000000)
        slider22.set(float(master.pri_attachment_pt_range_x3.get()))
        slider22.grid(row=row, column=2, padx=20, pady=10)

        input19_1.bind('<KeyRelease>', input_event(input19_1, slider20, 'pri_attachment_pt_range_x1'))
        input19_2.bind('<KeyRelease>', input_event(input19_2, slider21, 'pri_attachment_pt_range_x2'))
        input19_3.bind('<KeyRelease>', input_event(input19_3, slider22, 'pri_attachment_pt_range_x3'))
        
        row += 1

        divider_10 = tk.Label(master=self)
        divider_10.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1
        
        # ------ pricing_range ------ #
        label20 = ctk.CTkLabel(master=self, text='pricing_range:\n' + str('(def: '+str(master.defaults['pricing_range'])+')'), font=('Arial', 14, 'bold'))
        label20.grid(row=row, column=0, padx=10, pady=20)

        input20 = ctk.CTkEntry(
            master=self, textvariable=master.pricing_range,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input20.grid(row=row, column=1, padx=10, pady=20)

        slider22_1 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'pricing_range', 4))
        slider22_1.configure(number_of_steps=100000000)
        slider22_1.set(float(master.pricing_range.get()))
        slider22_1.grid(row=row, column=2, padx=20, pady=10)
        
        input20.bind('<KeyRelease>', input_event(input20, slider22_1, 'pricing_range'))

        row += 1

        # ------ sme_pricing_low ------ #
        label21 = ctk.CTkLabel(master=self, text='sme_pricing_low:\n' + str('(def: '+str(master.defaults['sme_pricing_low'])+')'), font=('Arial', 14, 'bold'))
        label21.grid(row=row, column=0, padx=10, pady=20)

        input21 = ctk.CTkEntry(
            master=self, textvariable=master.sme_pricing_low,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input21.grid(row=row, column=1, padx=10, pady=20)


        # ------ sme_pricing_high ------ #
        label22 = ctk.CTkLabel(master=self, text='sme_pricing_high:\n' + str('(def: '+str(master.defaults['sme_pricing_high'])+')'), font=('Arial', 14, 'bold'))
        label22.grid(row=row, column=2, padx=10, pady=20)

        input22 = ctk.CTkEntry(
            master=self, textvariable=master.sme_pricing_high,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input22.grid(row=row, column=3, padx=10, pady=20)


        row += 1

        slider23 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'sme_pricing_low', 4))
        slider23.configure(number_of_steps=100000000)
        slider23.set(float(master.sme_pricing_low.get()))
        slider23.grid(row=row, column=1, padx=20, pady=10)

        slider24 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'sme_pricing_high', 4))
        slider24.configure(number_of_steps=100000000)
        slider24.set(float(master.sme_pricing_high.get()))
        slider24.grid(row=row, column=3, padx=20, pady=10)

        input21.bind('<KeyRelease>', input_event(input21, slider23, 'sme_pricing_low'))
        input22.bind('<KeyRelease>', input_event(input22, slider24, 'sme_pricing_high'))

        row += 1

        # ------ mm_pricing_low ------ #
        label23 = ctk.CTkLabel(master=self, text='mm_pricing_low:\n' + str('(def: '+str(master.defaults['mm_pricing_low'])+')'), font=('Arial', 14, 'bold'))
        label23.grid(row=row, column=0, padx=10, pady=20)

        input23 = ctk.CTkEntry(
            master=self, textvariable=master.mm_pricing_low,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input23.grid(row=row, column=1, padx=10, pady=20)


        # ------ mm_pricing_high ------ #
        label24 = ctk.CTkLabel(master=self, text='mm_pricing_high:\n' + str('(def: '+str(master.defaults['mm_pricing_high'])+')'), font=('Arial', 14, 'bold'))
        label24.grid(row=row, column=2, padx=10, pady=20)

        input24 = ctk.CTkEntry(
            master=self, textvariable=master.mm_pricing_high,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input24.grid(row=row, column=3, padx=10, pady=20)
        
        row += 1

        slider25 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'mm_pricing_low', 4))
        slider25.configure(number_of_steps=100000000)
        slider25.set(float(master.mm_pricing_low.get()))
        slider25.grid(row=row, column=1, padx=20, pady=10)

        slider26 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'mm_pricing_high', 4))
        slider26.configure(number_of_steps=100000000)
        slider26.set(float(master.mm_pricing_high.get()))
        slider26.grid(row=row, column=3, padx=20, pady=10)

        input23.bind('<KeyRelease>', input_event(input23, slider25, 'mm_pricing_low'))
        input24.bind('<KeyRelease>', input_event(input24, slider26, 'mm_pricing_high'))

        row += 1
        
        divider_10 = tk.Label(master=self)
        divider_10.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1

        # ------ j_pricing_low ------ #
        label25 = ctk.CTkLabel(master=self, text='j_pricing_low:\n' + str('(def: '+str(master.defaults['j_pricing_low'])+')'), font=('Arial', 14, 'bold'))
        label25.grid(row=row, column=0, padx=10, pady=20)

        input25 = ctk.CTkEntry(
            master=self, textvariable=master.j_pricing_low,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input25.grid(row=row, column=1, padx=10, pady=20)


        # ------ j_pricing_high ------ #
        label26 = ctk.CTkLabel(master=self, text='j_pricing_high:\n' + str('(def: '+str(master.defaults['j_pricing_low'])+')'), font=('Arial', 14, 'bold'))
        label26.grid(row=row, column=2, padx=10, pady=20)

        input26 = ctk.CTkEntry(
            master=self, textvariable=master.j_pricing_high,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input26.grid(row=row, column=3, padx=10, pady=20)

        row += 1

        slider27 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'j_pricing_low', 4))
        slider27.configure(number_of_steps=100000000)
        slider27.set(float(master.j_pricing_low.get()))
        slider27.grid(row=row, column=1, padx=20, pady=10)

        slider28 = ctk.CTkSlider(self, from_=0.00001, to=0.99999, command=lambda value: slider_event_float(value, 'j_pricing_high', 4))
        slider28.configure(number_of_steps=100000000)
        slider28.set(float(master.j_pricing_high.get()))
        slider28.grid(row=row, column=3, padx=20, pady=10)

        input25.bind('<KeyRelease>', input_event(input25, slider27, 'j_pricing_low'))
        input26.bind('<KeyRelease>', input_event(input26, slider28, 'j_pricing_high'))

        row += 1
        
        divider_10 = tk.Label(master=self)
        divider_10.grid(row=row, column=0, columnspan=4, sticky='ew', padx=0, pady=30)
        
        row += 1

        # ------ low_low_severity_loss ------ #
        label27 = ctk.CTkLabel(master=self, text='low_low_severity_loss:\n' + str('(def: '+str(master.defaults['low_low_severity_loss'])+')'), font=('Arial', 14, 'bold'))
        label27.grid(row=row, column=0, padx=10, pady=20)

        input27 = ctk.CTkEntry(
            master=self, textvariable=master.low_low_severity_loss,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input27.grid(row=row, column=1, padx=10, pady=20)


        # ------ low_high_severity_loss ------ #
        label28 = ctk.CTkLabel(master=self, text='low_high_severity_loss:\n' + str('(def: '+str(master.defaults['low_high_severity_loss'])+')'), font=('Arial', 14, 'bold'))
        label28.grid(row=row, column=2, padx=10, pady=20)

        input28 = ctk.CTkEntry(
            master=self, textvariable=master.low_high_severity_loss,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input28.grid(row=row, column=3, padx=10, pady=20)

        row += 1

        slider29 = ctk.CTkSlider(self, from_=0, to=100000, command=lambda value: slider_event_int(value, 'low_low_severity_loss'))
        slider29.configure(number_of_steps=10000000)
        slider29.set(int(master.low_low_severity_loss.get()))
        slider29.grid(row=row, column=1, padx=20, pady=0)


        slider30 = ctk.CTkSlider(self, from_=0, to=(int(master.low_high_severity_loss.get())*2), command=lambda value: slider_event_int(value, 'low_high_severity_loss'))
        slider30.configure(number_of_steps=(int(master.low_high_severity_loss.get())*2*100000))
        slider30.set(int(master.low_high_severity_loss.get()))
        slider30.grid(row=row, column=3, padx=20, pady=0)

        input27.bind('<KeyRelease>', input_event(input27, slider29, 'low_low_severity_loss'))
        input28.bind('<KeyRelease>', input_event(input28, slider30, 'low_high_severity_loss'))

        row += 1

        # ------ med_low_severity_loss ------ #
        label29 = ctk.CTkLabel(master=self, text='med_low_severity_loss:\n' + str('(def: '+str(master.defaults['med_low_severity_loss'])+')'), font=('Arial', 14, 'bold'))
        label29.grid(row=row, column=0, padx=10, pady=20)

        input29 = ctk.CTkEntry(
            master=self, textvariable=master.med_low_severity_loss,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input29.grid(row=row, column=1, padx=10, pady=20)
    

        # ------ med_high_severity_loss ------ #
        label30 = ctk.CTkLabel(master=self, text='med_high_severity_loss:\n' + str('(def: '+str(master.defaults['med_high_severity_loss'])+')'), font=('Arial', 14, 'bold'))
        label30.grid(row=row, column=2, padx=10, pady=20)

        input30 = ctk.CTkEntry(
            master=self, textvariable=master.med_high_severity_loss,
            validate='key', validatecommand=(float_validation, '%P')
        )
        input30.grid(row=row, column=3, padx=10, pady=20)

        row += 1

        slider31 = ctk.CTkSlider(self, from_=0, to=(int(master.med_low_severity_loss.get())*2), command=lambda value: slider_event_int(value, 'med_low_severity_loss'))
        slider31.configure(number_of_steps=(int(master.med_low_severity_loss.get())*2*100000))
        slider31.set(int(master.med_low_severity_loss.get()))
        slider31.grid(row=row, column=1, padx=20, pady=0)


        slider32 = ctk.CTkSlider(self, from_=0, to=(int(master.med_high_severity_loss.get())*2), command=lambda value: slider_event_int(value, 'med_high_severity_loss'))
        slider32.configure(number_of_steps=(int(master.med_high_severity_loss.get())*2*100000))
        slider32.set(int(master.med_high_severity_loss.get()))
        slider32.grid(row=row, column=3, padx=20, pady=0)

        input29.bind('<KeyRelease>', input_event(input29, slider31, 'med_low_severity_loss'))
        input30.bind('<KeyRelease>', input_event(input30, slider32, 'med_high_severity_loss'))

        row += 1


        # ------ Submit button ------ #
        self.submit_button = ctk.CTkButton(master=self, command=master.start_calculation, text='Start calculation', font=('Arial', 16, 'bold'))
        self.submit_button.grid(row=row, column=0, columnspan=4, padx=20, pady=40)

        row += 1

        self.label_error = ctk.CTkLabel(master=self, text='', font=('Arial', 14, 'bold'), text_color='red')
        self.label_error.grid(row=row, columnspan=4, padx=10, pady=20)

    def start_loader(self):
        self.loader.start()

    def stop_loader(self):
        self.loader.stop()


class ResultFrame(ctk.CTkFrame):
    def __init__(self, master, form_data, **kwargs):
        super().__init__(master, **kwargs)

        row = 0

        # Define variables
        self.percentage_of_scenarios_above_zero = tk.StringVar(value=0)
        self.percentage_of_scenarios_above_1m = tk.StringVar(value=0)
        self.percentage_of_scenarios_above_10m = tk.StringVar(value=0)

        self.average = tk.StringVar(value=0)
        self.max = tk.StringVar(value=0)
        self.min = tk.StringVar(value=0)

        self.graph = tk.StringVar()


        # ------ Title of frame ------ #
        res_title = ctk.CTkLabel(master=self, text='Result', font=('Arial', 18, 'bold'))
        res_title.grid(row=row, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        row += 1

        res_label_1 = ctk.CTkLabel(master=self, text='Percentage of scenarios above 0:', font=('Arial', 14, 'bold'))
        res_label_1.grid(row=row, column=0,  padx=10, pady=10, sticky='nsew')

        res_label_2 = ctk.CTkLabel(master=self, textvariable=self.percentage_of_scenarios_above_zero, font=('Arial', 14, 'bold'))
        res_label_2.grid(row=row, column=1, padx=10, pady=10, sticky='nsew')


        res_fake_1 = ctk.CTkLabel(master=self, text='', font=('Arial', 14, 'bold'))
        res_fake_1.grid(row=row, column=2, padx=10, pady=10, sticky='nsew')


        res_label_6 = ctk.CTkLabel(master=self, text='Average:', font=('Arial', 14, 'bold'))
        res_label_6.grid(row=row, column=3, padx=10, pady=10, sticky='nsew')

        res_label_7 = ctk.CTkLabel(master=self, textvariable=self.average, font=('Arial', 14, 'bold'))
        res_label_7.grid(row=row, column=4, padx=10, pady=10, sticky='nsew')

        row += 1

        res_label_3 = ctk.CTkLabel(master=self, text='Percentage of scenarios above 1m:', font=('Arial', 14, 'bold'))
        res_label_3.grid(row=row, column=0, padx=10, pady=10, sticky='nsew')

        res_label_4 = ctk.CTkLabel(master=self, textvariable=self.percentage_of_scenarios_above_1m, font=('Arial', 14, 'bold'))
        res_label_4.grid(row=row, column=1, padx=10, pady=10, sticky='nsew')


        res_fake_2 = ctk.CTkLabel(master=self, text='', font=('Arial', 14, 'bold'))
        res_fake_2.grid(row=row, column=2, padx=10, pady=10, sticky='nsew')


        res_label_8 = ctk.CTkLabel(master=self, text='Max:', font=('Arial', 14, 'bold'))
        res_label_8.grid(row=row, column=3, padx=10, pady=10, sticky='nsew')

        res_label_9 = ctk.CTkLabel(master=self, textvariable=self.max, font=('Arial', 14, 'bold'))
        res_label_9.grid(row=row, column=4, padx=10, pady=10, sticky='nsew')

        row += 1

        res_label_5 = ctk.CTkLabel(master=self, text='Percentage of scenarios above 10m:', font=('Arial', 14, 'bold'))
        res_label_5.grid(row=row, column=0, padx=10, pady=10, sticky='nsew')

        res_label_5 = ctk.CTkLabel(master=self, textvariable=self.percentage_of_scenarios_above_10m, font=('Arial', 14, 'bold'))
        res_label_5.grid(row=row, column=1, padx=10, pady=10, sticky='nsew')

        res_fake_3 = ctk.CTkLabel(master=self, text='', font=('Arial', 14, 'bold'))
        res_fake_3.grid(row=row, column=2, padx=10, pady=10, sticky='nsew')


        res_label_10 = ctk.CTkLabel(master=self, text='Min:', font=('Arial', 14, 'bold'))
        res_label_10.grid(row=row, column=3, padx=10, pady=10, sticky='nsew')

        res_label_11 = ctk.CTkLabel(master=self, textvariable=self.min, font=('Arial', 14, 'bold'))
        res_label_11.grid(row=row, column=4, padx=10, pady=10, sticky='nsew')

        row += 1

        self.res_label_12 = ctk.CTkLabel(master=self, text='')
        self.res_label_12.grid(row=row, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')


    # Update variables
    def update_results(self, result_data):
        for key, value in result_data.items():
            item = getattr(self, key)
            item.set(value)

        # Convert the graph to an image
        image_data = io.BytesIO()
        result_data['graph'].savefig(image_data, format='png')
        image_data.seek(0)

        # Create a Tkinter-compatible image
        image = ImageTk.PhotoImage(Image.open(image_data))

        # Display the image in the GUI
        self.res_label_12.configure(image=image)
        self.res_label_12.image = image


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        # Data from form
        self.form_data = {
            'num_simulations': 1000,

            'notice_pct_dist_x1': .05,
            'notice_pct_dist_x2': .15,
            'notice_pct_dist_x3': .25,
            'notice_pct_dist_x4': 100_000,

            'notice_pct_loss_dist_x1': .15,
            'notice_pct_loss_dist_x2': .25,
            'notice_pct_loss_dist_x3': .35,
            'notice_pct_loss_dist_x4': 100_000,

            'severity_dist_x1': .65,
            'severity_dist_x2': .75,
            'severity_dist_x3': .85,
            'severity_dist_x4': 100_000,

            'deal_count': 100,
            'DV_range': 2_500_000,

            'sme_low_DV': 10_000_000,
            'sme_upper_DV': 75_000_000,

            'mm_low_DV': 75_000_000,
            'mm_upper_DV': 750_000_000,

            'sme_pct': .35,
            'mm_pct': .55,
            'j_pct': .1,

            'j_low_DV': 750_000_000,
            'j_upper_DV': 5_000_000_000,

            'low_limit': 30_000_000,
            'upper_limit': 50_000_000,
            'limit_range': 2_500_000,

            'primary_pct': .7,
            'xs_pct': .3,

            'pri_attachment_pt_range_x1': 0.0025,
            'pri_attachment_pt_range_x2': 0.005,
            'pri_attachment_pt_range_x3': 0.0005,

            'pricing_range': .05,

            'sme_pricing_low': .012,
            'sme_pricing_high': .0145,

            'mm_pricing_low': .0135,
            'mm_pricing_high': .0165,

            'j_pricing_low': .035,
            'j_pricing_high': .075,
            
            'low_low_severity_loss': 0,
            'low_high_severity_loss': 1_000_000,

            'med_low_severity_loss': 1_000_000,
            'med_high_severity_loss': 10_000_000,
        }

        self.defaults = self.form_data.copy()

        # Data binding variables
        self.num_simulations = tk.IntVar(value=str(self.form_data['num_simulations']))

        self.notice_pct_dist_x1 = tk.StringVar(value=str(self.form_data['notice_pct_dist_x1']))
        self.notice_pct_dist_x2 = tk.StringVar(value=str(self.form_data['notice_pct_dist_x2']))
        self.notice_pct_dist_x3 = tk.StringVar(value=str(self.form_data['notice_pct_dist_x3']))
        self.notice_pct_dist_x4 = tk.IntVar(value=str(self.form_data['notice_pct_dist_x4']))

        self.notice_pct_loss_dist_x1 = tk.StringVar(value=str(self.form_data['notice_pct_loss_dist_x1']))
        self.notice_pct_loss_dist_x2 = tk.StringVar(value=str(self.form_data['notice_pct_loss_dist_x2']))
        self.notice_pct_loss_dist_x3 = tk.StringVar(value=str(self.form_data['notice_pct_loss_dist_x3']))
        self.notice_pct_loss_dist_x4 = tk.IntVar(value=str(self.form_data['notice_pct_loss_dist_x4']))

        self.severity_dist_x1 = tk.StringVar(value=str(self.form_data['severity_dist_x1']))
        self.severity_dist_x2 = tk.StringVar(value=str(self.form_data['severity_dist_x2']))
        self.severity_dist_x3 = tk.StringVar(value=str(self.form_data['severity_dist_x3']))
        self.severity_dist_x4 = tk.IntVar(value=str(self.form_data['severity_dist_x4']))

        self.deal_count = tk.IntVar(value=str(self.form_data['deal_count']))
        
        self.DV_range = tk.IntVar(value=str(self.form_data['DV_range']))

        self.sme_low_DV = tk.IntVar(value=str(self.form_data['sme_low_DV']))
        self.sme_upper_DV = tk.IntVar(value=str(self.form_data['sme_upper_DV']))
        
        self.mm_low_DV = tk.IntVar(value=str(self.form_data['mm_low_DV']))
        self.mm_upper_DV = tk.IntVar(value=str(self.form_data['mm_upper_DV']))

        self.sme_pct = tk.StringVar(value=str(self.form_data['sme_pct']))
        self.mm_pct = tk.StringVar(value=str(self.form_data['mm_pct']))
        self.j_pct = tk.StringVar(value=str(self.form_data['j_pct']))

        self.j_low_DV = tk.IntVar(value=str(self.form_data['j_low_DV']))
        self.j_upper_DV = tk.IntVar(value=str(self.form_data['j_upper_DV']))

        self.low_limit = tk.IntVar(value=str(self.form_data['low_limit']))
        self.upper_limit = tk.IntVar(value=str(self.form_data['upper_limit']))
        self.limit_range = tk.IntVar(value=str(self.form_data['limit_range']))

        self.primary_pct = tk.StringVar(value=str(self.form_data['primary_pct']))
        self.xs_pct = tk.StringVar(value=str(self.form_data['xs_pct']))

        self.pri_attachment_pt_range_x1 = tk.StringVar(value=str(self.form_data['pri_attachment_pt_range_x1']))
        self.pri_attachment_pt_range_x2 = tk.StringVar(value=str(self.form_data['pri_attachment_pt_range_x2']))
        self.pri_attachment_pt_range_x3 = tk.StringVar(value=str(self.form_data['pri_attachment_pt_range_x3']))
        
        self.pricing_range = tk.StringVar(value=str(self.form_data['pricing_range']))

        self.sme_pricing_low = tk.StringVar(value=str(self.form_data['sme_pricing_low']))
        self.sme_pricing_high = tk.StringVar(value=str(self.form_data['sme_pricing_high']))

        self.mm_pricing_low = tk.StringVar(value=str(self.form_data['mm_pricing_low']))
        self.mm_pricing_high = tk.StringVar(value=str(self.form_data['mm_pricing_high']))

        self.j_pricing_low = tk.StringVar(value=str(self.form_data['j_pricing_low']))
        self.j_pricing_high = tk.StringVar(value=str(self.form_data['j_pricing_high']))
        
        self.low_low_severity_loss = tk.IntVar(value=str(self.form_data['low_low_severity_loss']))
        self.low_high_severity_loss = tk.IntVar(value=str(self.form_data['low_high_severity_loss']))

        self.med_low_severity_loss = tk.IntVar(value=str(self.form_data['med_low_severity_loss']))
        self.med_high_severity_loss = tk.IntVar(value=str(self.form_data['med_high_severity_loss']))
        
        # Result data
        self.result_data = {}

        row = 0

        # Close button
        self.close_button = ctk.CTkButton(self, text="Close", command=master.close_window)
        self.close_button.grid(row=row, column=3, padx=20, pady=20,)

        row += 1

        # Form wrapper
        self.form_frame = FormFrame(master=self, form_data=self.form_data)
        self.form_frame.grid(row=row, columnspan=4, padx=20, pady=20, sticky='nsew')

        row += 1

        # Result wrapper
        self.result_frame = ResultFrame(master=self, form_data=self.result_data)
        self.result_frame.grid(row=row, columnspan=4, padx=20, pady=20, sticky='')


    def start_calculation(self):
        self.form_frame.label_error.configure(text='')
        self.form_frame.submit_button.configure(text='Calculating ...')

        thread = threading.Thread(target=self.perform_calculation)
        thread.start()

    def perform_calculation(self):
        try:
            result = asyncio.run(main_func(self.form_data))
            self.after(200, partial(self.update_results_in_main_thread, result))
        except Exception as e:
            try:
                self.after(200, partial(self.show_error_message, str(e)+'\n'+str('More details in console')))
                self.form_frame.submit_button.configure(text='Start calculation')
                traceback.print_exc()
            except:
                pass
                


    def update_results_in_main_thread(self, result):
        self.result_data = result
        self.result_frame.update_results(self.result_data)
        self.form_frame.submit_button.configure(text='Start calculation')

    def show_error_message(self, error_message):
        self.form_frame.label_error.configure(text=error_message)
        self.form_frame.submit_button.configure(text='Start calculation')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration app window
        self.title('Insurance Calc')
        self.geometry('1020x1000')
        self.resizable(width=True, height=True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Scroll wrapper
        self.scroll_frame = ScrollFrame(master=self, width=980, height=960, fg_color='transparent')
        self.scroll_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

    def close_window(self):
        self.destroy()

app = App()
app.mainloop()
