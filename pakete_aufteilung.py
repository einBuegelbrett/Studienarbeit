import pandas as pd
from datetime import datetime, timedelta

# Daten laden
df = pd.read_csv('/home/sven/Dokumente/dhbw/studienarbeit/Studienarbeit/rennen5.csv', sep=',')

df['timestamp'] = pd.to_datetime(df['timestamp'])

# Nach Zeit sortieren
df = df.sort_values('timestamp').reset_index(drop=True)

# Labels definieren 
labels = ['rennen']
num_segments = len(labels)

# Länge jedes Abschnitts (nach Anzahl Zeilen)
segment_length = len(df) // num_segments

packet_counter = 333

# Jeden Abschnitt verarbeiten
for i in range(num_segments):
    start_idx = i * segment_length
    end_idx = (i + 1) * segment_length if i < num_segments - 1 else len(df)
    
    segment_df = df.iloc[start_idx:end_idx].copy()
    segment_label = labels[i]
    
    # Segment-Zeitgrenzen
    segment_df = segment_df.sort_values('timestamp').reset_index(drop=True)
    start_time = segment_df['timestamp'].iloc[0]
    end_time = segment_df['timestamp'].iloc[-1]
    
    # 5-Sekunden-Pakete innerhalb des Segments
    current_start = start_time
    packet_duration = timedelta(seconds=5)
    
    while current_start < end_time:
        current_end = current_start + packet_duration
        mask = (segment_df['timestamp'] >= current_start) & (segment_df['timestamp'] < current_end)
        packet_df = segment_df.loc[mask]
        
        if not packet_df.empty:
            packet_df = packet_df.sort_values('timestamp').reset_index(drop=True)

            # Timer-Spalte erstellen
            timer = [0.0]
            for j in range(1, len(packet_df)):
                delta = (packet_df.loc[j, 'timestamp'] - packet_df.loc[j - 1, 'timestamp']).total_seconds()
                timer.append(timer[-1] + delta)
            
            packet_df['Timer'] = timer

            # timestamp entfernen
            packet_df = packet_df.drop(columns=['timestamp'])

            # CSV speichern
            packet_df.to_csv(
                f'/home/sven/Dokumente/dhbw/studienarbeit/Studienarbeit/daten/packet_{packet_counter}_{segment_label}.csv', index=False
            )
            packet_counter += 1
        
        current_start = current_end

print("Daten wurden in 5-Sekunden-Pakete mit Labels im Dateinamen aufgeteilt.")
