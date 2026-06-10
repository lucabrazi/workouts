# Video Addition Workflow

This document outlines the standard process for adding or replacing exercise demonstration videos in the Workout Tracker app. Following this workflow prevents broken video embeds (e.g., YouTube `Error 153` due to disabled playback on other websites) and ensures high-quality form tutorials.

---

## The Workflow

### 1. Identify Target Exercises
Find the exercises that need video links by locating the `<button class="info-icon">` elements in [index.html](../index.html).
*   Note the exact exercise name inside the `data-name` attribute or the adjacent `.exercise-name` span.

### 2. Query YouTube for Candidates
Search YouTube for demonstration tutorials. 
*   **Search Queries:** Use targeted search strings like `"{Exercise Name} form check tutorial male"` or `"{Exercise Name} exercise female form tutorial"` depending on project constraints.
*   **Preferred Channels:** Prioritize reputable, professional physical therapy and training channels that demonstrate clean form (e.g., *Squat University*, *Mind Pump TV*, *Daily Workout Builder*, *Rehab Hero*, *RehabFix*, *Functional Bodybuilding*, etc.).

### 3. Verify Embeddability Programmatically
Do **not** assume every YouTube video is embeddable. Many creators disable external embeds, causing the player to crash in the app.

To check if a video is embeddable, query the official **YouTube oEmbed API**:
```http
GET https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=VIDEO_ID&format=json
```

**Python Helper Script (`verify_video.py`):**
```python
import urllib.request
import urllib.parse
import json

def check_video_embeddability(video_id):
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    try:
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print(f"[OK] Title: {data.get('title')} | Author: {data.get('author_name')}")
                return True
    except Exception as e:
        print(f"[FAILED] Video {video_id} is restricted or does not exist: {e}")
        return False
```
*   **`OK`:** The video allows embedding and is safe to use.
*   **`FAILED` (returns HTTP 401 or 404):** The video has disabled external embeds or is private/deleted. **Do not use it.**

### 4. Vet the Content
Inspect the JSON response from the oEmbed API (or open the link in a browser):
*   Check the video title and the `author_name` (channel) to confirm the presenter matches the requested criteria (e.g., specific gender, correct equipment, or specific style of stretch).

### 5. Inject Into the HTML Structure
Add the `data-video` attribute with the full YouTube watch URL to the corresponding `.info-icon` button:
```html
<li>
    <label class="exercise-label">
        <input type="checkbox">
        <span class="exercise-name">Example Exercise</span>
        <span class="exercise-reps">10 reps</span>
    </label>
    <button class="info-icon" 
            data-name="Example Exercise" 
            data-desc="Description of exercise here." 
            data-video="https://www.youtube.com/watch?v=VIDEO_ID" 
            onclick="openInfoModal(event, this)">i</button>
</li>
```

### 6. Manual Verification Check
1.  Open [index.html](../index.html) in your browser.
2.  Navigate to the day tab and click the **"i" (Info)** button of the modified exercise.
3.  Confirm the **"Watch Video"** button is displayed.
4.  Click the button to open the fullscreen video overlay modal.
5.  Ensure the video starts playing and renders correctly within the iframe player.
