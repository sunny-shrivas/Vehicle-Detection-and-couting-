'''Streamlit interface for VehicleFlow.'''
import time
from pathlib import Path
import cv2
import pandas as pd
import streamlit as st
from vehicle_counter.pipeline import VehicleCountingPipeline

st.set_page_config(page_title='VehicleFlow | Traffic Analytics', page_icon='🚗', layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem;max-width:1440px}[data-testid="stMetric"]{background:rgba(120,130,150,.08);border:1px solid rgba(120,130,150,.18);padding:16px;border-radius:14px}.hero{padding:24px;border:1px solid rgba(120,130,150,.24);border-radius:18px;background:linear-gradient(120deg,rgba(20,184,166,.12),rgba(59,130,246,.08))}</style>''', unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>🚦 VehicleFlow</h1><p>Classical computer vision for traffic movement detection and virtual-line vehicle counting.</p><p>Python · OpenCV · Motion Detection · Centroid Tracking</p></div>', unsafe_allow_html=True)
with st.sidebar:
    st.header('Analysis settings')
    uploaded = st.file_uploader('Upload traffic video', type=['mp4', 'avi', 'mov', 'mkv'])
    line_ratio = st.slider('Counting line position', 0.1, 0.9, 0.6, 0.01)
    direction = st.selectbox('Count direction', ['down', 'up', 'both'])
    min_area = st.slider('Minimum moving-object area', 100, 5000, 650, 50)
    max_distance = st.slider('Tracker matching distance', 20, 180, 75, 5)
    width_threshold = st.slider('Large-vehicle width threshold', 30, 180, 70, 5)
    frame_stride = st.slider('Process every Nth frame', 1, 5, 1)
    start = st.button('Start analysis', type='primary', disabled=uploaded is None, use_container_width=True)
    st.caption('Best for fixed-camera video. Lighting changes, shadows, and overlapping vehicles affect reliability.')
preview, metrics = st.columns([2, 1])
with preview:
    video_view = st.empty()
with metrics:
    total_metric, large_metric, small_metric = st.empty(), st.empty(), st.empty()
    progress = st.progress(0)
if uploaded is None:
    st.info('Upload a traffic video, configure the counting line, and start analysis.')
    st.markdown('### Processing flow\n1. Frame differencing detects moving regions.\n2. Contours become bounding-box detections.\n3. Centroid tracking links objects across frames.\n4. A virtual line counts each track once.')
if start and uploaded is not None:
    suffix = Path(uploaded.name).suffix or '.mp4'
    temp = Path('temp_upload' + suffix)
    temp.write_bytes(uploaded.getbuffer())
    cap = cv2.VideoCapture(str(temp))
    if not cap.isOpened():
        st.error('Could not open this clip. Try MP4 (H.264) or AVI.')
        temp.unlink(missing_ok=True)
    else:
        frame_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        pipeline = VehicleCountingPipeline(int(height * line_ratio), min_area, max_distance, direction, width_threshold)
        rows, frame_no, processed = [], 0, 0
        started = time.time()
        try:
            while cap.isOpened():
                ok, frame = cap.read()
                if not ok:
                    break
                frame_no += 1
                if frame_no % frame_stride:
                    continue
                tracks, _, _ = pipeline.process(frame)
                for track in tracks:
                    if track.missed_frames:
                        continue
                    x, y, w, h = track.bbox
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (30, 210, 150), 2)
                    cv2.putText(frame, 'ID ' + str(track.track_id), (x, max(20, y - 8)), cv2.FONT_HERSHEY_SIMPLEX, .55, (30, 210, 150), 2)
                line_y = int(height * line_ratio)
                cv2.line(frame, (0, line_y), (width, line_y), (40, 150, 255), 2)
                cv2.putText(frame, 'Count: ' + str(pipeline.counter.total), (20, 35), cv2.FONT_HERSHEY_SIMPLEX, .9, (255, 255, 255), 2)
                video_view.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels='RGB', use_container_width=True)
                total_metric.metric('Vehicles counted', pipeline.counter.total)
                large_metric.metric('Larger width group', pipeline.large_count)
                small_metric.metric('Smaller width group', pipeline.small_count)
                rows.append({'frame': frame_no, 'timestamp_seconds': round(frame_no / fps, 2) if fps else None, 'total_count': pipeline.counter.total, 'large_width_group': pipeline.large_count, 'small_width_group': pipeline.small_count, 'active_tracks': sum(t.missed_frames == 0 for t in tracks)})
                processed += 1
                if frame_total:
                    progress.progress(min(frame_no / frame_total, 1.0))
                if processed % 10 == 0:
                    st.caption('Processed ' + str(frame_no) + '/' + str(frame_total or '?') + ' frames · ' + str(round(time.time() - started, 1)) + 's elapsed')
            st.success('Finished: ' + str(pipeline.counter.total) + ' line crossings counted across ' + str(processed) + ' processed frames.')
            if rows:
                report = pd.DataFrame(rows)
                st.subheader('Count timeline')
                st.line_chart(report.set_index('frame')[['total_count']])
                st.download_button('Download count report (CSV)', report.to_csv(index=False), 'vehicle_count_report.csv', 'text/csv')
                st.dataframe(report.tail(20), use_container_width=True)
        finally:
            cap.release()
            temp.unlink(missing_ok=True)
st.divider()
st.caption('Research/demo prototype. Counts depend on camera angle, scene density, lighting, object overlap, and tuned thresholds. Not intended for safety-critical or enforcement use.')
