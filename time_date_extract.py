import re
from datetime import datetime


class TimeDateFinder:
    @staticmethod
    def time_date_extract(t: str) -> str:
        date_time_finder = r'\b(\d{4})[-\/](0?[1-9]|1[0-2])[-\/](0?[1-9]|[12][0-9]|3[01])\s(0?[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])\b'
        months = r'(\d{1,2}(?:st|nd|rd|th)?\s)?(?:January|February|March|April|May|June|July|August|September|October|November|December)'
        time_finder = r'\b(0?[0-9]|1[0-9]|2[0-3]):([0-5][0-9])(?:am|pm)?\b'

        text_l = t.split(' ')
        result = []

        for i, part in enumerate(text_l):
            if re.search(months, part):
                temp_apnd = [part]

                if i + 1 < len(text_l):
                    temp_apnd.append(text_l[i + 1].rstrip(',.'))

                if i + 2 < len(text_l) and text_l[i + 2][0].isdigit():
                    temp_apnd.append(text_l[i + 2])
                elif i + 3 < len(text_l):
                    temp_apnd.append(text_l[i + 3])

                result.append(' '.join(temp_apnd))
            elif re.findall(date_time_finder, part):
                if i + 2 < len(text_l):
                    time_part = f'{text_l[i + 2]} {text_l[i + 3]}'
                    if re.search(time_finder, time_part):
                        result.append(f'{text_l[i]} {time_part}')

            elif re.findall(time_finder, part):
                result.append(part)

        return '\n'.join(result)


input_text = "Hi, my name is Jane and my phone number is 555-123-4567. My email address is jane_doe@example.com. I live on 123 Main St. Apt. #456, and I was born on January  11th, 1990. I have an appointment on 2023-05-15 at 2:30pm at 789 Oak Ln. #3 and backup on 2023/ 05/21. Please give me a call or send me an email to confirm. In case the dates are unavailable, please set up a meeting sometime in June. I would love June 19th around 14:00. Thank you!"

if __name__ == "__main__":
    print(f"Extracted time and dates are:\n{TimeDateFinder.time_date_extract(input_text)}")
