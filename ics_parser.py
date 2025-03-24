import re
from datetime import datetime, timedelta
import sys
from pathlib import Path

def parse_ics_file(file_path):
    """
    Parse an ICS file and extract event information.
    
    Args:
        file_path (str): Path to the ICS file
        
    Returns:
        tuple: (calendar_info, events_list)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}, []
    
    # Extract calendar information
    calendar_info = {}
    cal_name_match = re.search(r'X-WR-CALNAME:(.*?)(?:\r\n|\n)', content)
    if cal_name_match:
        calendar_info['NAME'] = cal_name_match.group(1)
    
    timezone_match = re.search(r'X-WR-TIMEZONE:(.*?)(?:\r\n|\n)', content)
    if timezone_match:
        calendar_info['TIMEZONE'] = timezone_match.group(1)
    
    # Split the content by event
    event_blocks = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', content, re.DOTALL)
    
    events = []
    for block in event_blocks:
        event = {}
        
        # Extract the fields we're interested in
        created_match = re.search(r'CREATED:(.*?)(?:\r\n|\n)', block)
        if created_match:
            created_timestamp = created_match.group(1)
            event['CREATED'] = manual_format_timestamp(created_timestamp, 1)
            
        dtstart_match = re.search(r'DTSTART(?:;[^:]*)?:(.*?)(?:\r\n|\n)', block)
        if dtstart_match:
            dtstart_timestamp = dtstart_match.group(1)
            event['DTSTART'] = manual_format_timestamp(dtstart_timestamp, 2)
        
        dtend_match = re.search(r'DTEND(?:;[^:]*)?:(.*?)(?:\r\n|\n)', block)
        if dtend_match:
            dtend_timestamp = dtend_match.group(1)
            event['DTEND'] = manual_format_timestamp(dtend_timestamp, 2)
            
        summary_match = re.search(r'SUMMARY:(.*?)(?:\r\n|\n)', block)
        if summary_match:
            event['SUMMARY'] = summary_match.group(1)
        
        if event:  # Only add if we found at least one field
            events.append(event)
    
    return calendar_info, events

def manual_format_timestamp(timestamp, hour_adjustment):
    """
    Manually parse and format an iCalendar timestamp with hour adjustment
    
    Args:
        timestamp (str): iCalendar timestamp string like "20250402T120000Z"
        hour_adjustment (int): Number of hours to adjust the timestamp by
        
    Returns:
        str: Formatted date and time
    """
    try:
        # Remove Z if present
        if timestamp.endswith('Z'):
            timestamp = timestamp[:-1]
        
        # Handle timestamps with T separator
        if 'T' in timestamp:
            date_part, time_part = timestamp.split('T')
            
            # Parse date components
            year = date_part[0:4]
            month = date_part[4:6]
            day = date_part[6:8]
            
            # Parse time components
            hour = int(time_part[0:2])
            minute = time_part[2:4]
            second = time_part[4:6]
            
            # Add the specified number of hours
            hour += hour_adjustment
            if hour >= 24:
                hour -= 24
                # This is a simplified approach - for proper day rollover,
                # we would need more complex date arithmetic
            
            # Format with padded hour
            hour_str = f"{hour:02d}"
            formatted_time = f"{hour_str}:{minute}:{second}"
            formatted_date = f"{day}/{month}/{year[2:4]}"
            
            formatted_timestamp = f"{formatted_time} {formatted_date}"
            return formatted_timestamp
        else:
            # Just a date, no time component
            year = timestamp[0:4]
            month = timestamp[4:6]
            day = timestamp[6:8]
            
            # Format date only (with 00:00:00 as time)
            formatted_timestamp = f"00:00:00 {day}/{month}/{year[2:4]}"
            return formatted_timestamp
            
    except Exception as e:
        # If anything goes wrong, return error message
        return f"Error: {timestamp}"

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default to looking for .ics files in current directory
        ics_files = list(Path('.').glob('*.ics'))
        if not ics_files:
            print("No .ics files found in current directory. Please specify a file path.")
            return
        file_path = ics_files[0]
        print(f"Using file: {file_path}")
    
    calendar_info, events = parse_ics_file(file_path)
    
    # Display calendar information
    print("\nCalendar Information:")
    print(f"  Name: {calendar_info.get('NAME', 'N/A')}")
    print(f"  Timezone: {calendar_info.get('TIMEZONE', 'N/A')}")
    
    if events:
        print(f"\nFound {len(events)} events:\n")
        for i, event in enumerate(events, 1):
            print(f"Event {i}:")
            print(f"  Summary:  {event.get('SUMMARY', 'N/A')}")
            print(f"  Created:  {event.get('CREATED', 'N/A')}")
            print(f"  Start:    {event.get('DTSTART', 'N/A')}")
            print(f"  End:      {event.get('DTEND', 'N/A')}")
            print()
    else:
        print("No events found in the file.")

if __name__ == "__main__":
    main()