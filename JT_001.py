from json import loads
from datetime import datetime


class EventOverlapCheck:
    @staticmethod
    def checker(evt: str) -> str:
        evt_dict, events_checked, overlaps = {}, [], []
        evt_list = evt.split(', ')

        # we'll store the events into a mapping table (dictionary) for faster lookup
        for e in evt_list:
            e_name, l_events = e.split(' = ')  # we get the event name and it's times
            evt_dict[e_name] = loads(l_events)  # using json loads to convert the stringed lists into proper lists

        dict_size = len(
            evt_dict)  # getting the lenght of the dictionary for use with a loop and having a dynamic name inside

        # we'll convert the times from H:M to total minutes for easier comparison and store them in a list
        for i in range(1, dict_size + 1):
            event_name = f"event_{i}"
            if event_name in evt_dict:
                event_start, event_end = evt_dict[event_name]
                start_minutes, end_minutes = datetime.strptime(event_start, "%H:%M").hour * 60 + datetime.strptime(
                    event_start, "%H:%M").minute, datetime.strptime(event_end, "%H:%M").hour * 60 + datetime.strptime(
                    event_end, "%H:%M").minute
                events_checked.append((start_minutes, end_minutes, event_name))

        # we sort the list so we can break the loop earlier and avoid unnecessary runs and check them in
        # chronological order
        events_checked.sort()

        # we'll go through every event in the sorted list and compare it with every other event to check for overlaps
        for i in range(dict_size): # get the current event to compare with the next events in (j)
            for j in range(i + 1, dict_size):
                # we unpack the event in comparison (i) with values sN(start time), eN(end time), evtN{event_(i) name)
                s1, e1, evt1 = events_checked[i]
                s2, e2, evt2 = events_checked[j]
                # we check if the end of i is less than the start of j, to avoid further checks and exit the loop early
                if e1 < s2:
                    break
                # we get the max of start from i and j and the min of i and j so we can get the
                # period which both events are active at the same time
                overlap_start, overlap_end = max(s1, s2), min(e1, e2)

                # here we call the helper function to get the H:M format as striing
                start_time = EventOverlapCheck.minutes_to_time_str(overlap_start)
                end_time = EventOverlapCheck.minutes_to_time_str(overlap_end)
                # and we append the information to be returned to the user
                overlaps.append(f"{evt1} overlaps with {evt2} from {start_time} to {end_time}")

        return ("true\n" + "\n".join(overlaps)) if overlaps else "false"

    @staticmethod
    def minutes_to_time_str(minutes: int) -> str:
        # this is a helper function to convert back minutes into HH:MM format
        return f"{minutes // 60:02d}:{minutes % 60:02d}"


if __name__ == '__main__':
    # we get the events from input as per example format:
    # Input: event_1 = ["02:15","04:00"], event_2 = ["04:00","06:00"]
    events = input('Please enter events:\n')
    print(EventOverlapCheck().checker(events))
