from tkinter import *
from functools import partial
from datetime import date

EXCHANGE_RATES = {
    ("USD", "NZD"): 1.6,
    ("NZD", "AUD"): 0.93,
    ("AUD", "USD"): 0.67,
    ("NZD", "USD"): 0.63,
    ("USD", "AUD"): 1.5,
    ("AUD", "NZD"): 1.08,
}


class Converter:
    def __init__(self):
        self.all_calculations_list = ['10 USD is 16.0 NZD', '20 NZD is 18.6 AUD',
                                      '50 AUD is 33.5 USD']

        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Currency Converter",
                                  font=("Arial", "16", "bold"))
        self.temp_heading.grid(row=0)

        instructions = ("Please enter an amount and press one of the buttons "
                        "to convert between USD, NZD, and AUD.")
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wraplength=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame, font=("Arial", "14"))
        self.temp_entry.grid(row=2, padx=10, pady=10)

        self.answer_error = Label(self.temp_frame, text="Please enter a number",
                                  fg="#004C99", font=("Arial", "14", "bold"))
        self.answer_error.grid(row=3)

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        # Button layout: 2 down, 3 across (grouped by from-currency per row)
        button_details_list = [
            # USD row (Row 0)
            ["USD to NZD", "#990099", lambda: self.check_amount("USD", "NZD"), 0, 0],
            ["USD to AUD", "#800000", lambda: self.check_amount("USD", "AUD"), 0, 1],

            # NZD row (Row 1)
            ["NZD to AUD", "#009900", lambda: self.check_amount("NZD", "AUD"), 1, 0],
            ["NZD to USD", "#336699", lambda: self.check_amount("NZD", "USD"), 1, 1],

            # AUD row (Row 2)
            ["AUD to USD", "#993333", lambda: self.check_amount("AUD", "USD"), 2, 0],
            ["AUD to NZD", "#336633", lambda: self.check_amount("AUD", "NZD"), 2, 1],

            # Utility row (Row 3)
            ["Help / Info", "#CC6600", self.to_help, 3, 0],
            ["History / Export", "#004C99", self.to_history, 3, 1],
        ]


        self.button_ref_list = []

        for item in button_details_list:
            self.make_button = Button(self.button_frame,
                                      text=item[0], bg=item[1],
                                      fg="#FFFFFF", font=("Arial", "12", "bold"),
                                      width=16, command=item[2])
            self.make_button.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(self.make_button)

        self.to_help_button = self.button_ref_list[6]
        self.to_history_button = self.button_ref_list[7]
        self.to_history_button.config(state=DISABLED)

    def check_amount(self, from_currency, to_currency):
        to_convert = self.temp_entry.get()

        self.answer_error.config(fg="#004C99", font=("Arial", "13", "bold"))
        self.temp_entry.config(bg="#FFFFFF")

        try:
            to_convert = float(to_convert)
            if to_convert >= 0:
                self.convert(from_currency, to_currency, to_convert)
            else:
                self.answer_error.config(text="Amount must be 0 or more", fg="#9C0000")
                self.temp_entry.config(bg="#F4CCCC")
                self.temp_entry.delete(0, END)
        except ValueError:
            self.answer_error.config(text="Please enter a number", fg="#9C0000")
            self.temp_entry.config(bg="#F4CCCC")
            self.temp_entry.delete(0, END)

    def convert(self, from_currency, to_currency, amount):
        rate = EXCHANGE_RATES.get((from_currency, to_currency), None)

        if rate is None:
            answer_statement = "Conversion not available."
        else:
            converted = round(amount * rate, 2)
            answer_statement = f"{amount} {from_currency} is {converted} {to_currency}"
            self.to_history_button.config(state=NORMAL)
            self.all_calculations_list.append(answer_statement)

        self.answer_error.config(text=answer_statement)

    def to_help(self):
        DisplayHelp(self)

    def to_history(self):
        HistoryExport(self, self.all_calculations_list)


class DisplayHelp:
    def __init__(self, partner):
        background = "#ffe6cc"
        self.help_box = Toplevel()
        partner.to_help_button.config(state=DISABLED)
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        text="Help / Info",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = ("To use the program, enter the amount of money you'd "
                     "like to convert. Then choose a conversion type "
                     "(e.g. USD to NZD). Exchange rates are approximate.\n\n"
                     "You can view your conversion history and export it to "
                     "a text file using the 'History / Export' button.")

        self.help_text_label = Label(self.help_frame,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        for item in [self.help_frame, self.help_heading_label]:
            item.config(bg=background)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


class HistoryExport:
    def __init__(self, partner, calculations):
        self.history_box = Toplevel()
        partner.to_history_button.config(state=DISABLED)
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        calc_back = "#D5E804"
        recent_intro_txt = "Below are all your currency conversions."

        newest_first_string = "\n".join(reversed(calculations))

        export_instruction_txt = ("Please push <Export> to save your calculations in "
                                  "a file. If the filename already exists, it will be overwritten.")

        history_labels_list = [
            ["History / Export", ("Arial", "16", "bold"), None],
            [recent_intro_txt, ("Arial", "11"), None],
            [newest_first_string, ("Arial", "14"), calc_back],
            [export_instruction_txt, ("Arial", "11"), None]
        ]

        self.export_filename_label = None

        for count, item in enumerate(history_labels_list):
            make_label = Label(self.history_box, text=item[0], font=item[1],
                               bg=item[2],
                               wraplength=300, justify="left", pady=10, padx=20)
            make_label.grid(row=count)
            if count == 3:
                self.export_filename_label = make_label

        self.hist_button_frame = Frame(self.history_box)
        self.hist_button_frame.grid(row=4)

        button_details_list = [
            ["Export", "#004C99", lambda: self.export_data(calculations), 0, 0],
            ["Close", "#666666", partial(self.close_history, partner), 0, 1],
        ]

        for btn in button_details_list:
            self.make_button = Button(self.hist_button_frame,
                                      font=("Arial", "12", "bold"),
                                      text=btn[0], bg=btn[1],
                                      fg="#FFFFFF", width=12,
                                      command=btn[2])
            self.make_button.grid(row=btn[3], column=btn[4], padx=10, pady=10)

    def export_data(self, calculations):
        today = date.today()
        file_name = f"currency_conversions_{today.strftime('%Y_%m_%d')}.txt"

        self.export_filename_label.config(fg="#009900",
                                          text=f"Export Successful! The file is called {file_name}",
                                          font=("Arial", "12", "bold"))

        with open(file_name, "w") as text_file:
            text_file.write("***** Currency Conversions *****\n")
            text_file.write(f"Generated: {today.strftime('%d/%m/%Y')}\n\n")
            text_file.write("Here is your calculation history (oldest to newest)...\n")
            for item in calculations:
                text_file.write(item + "\n")

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Currency Converter")
    Converter()
    root.mainloop()
