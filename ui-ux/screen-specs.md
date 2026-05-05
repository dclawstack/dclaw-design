# DClaw Video UI/UX Screen Specifications

## Design System
- Tailwind CSS with slate/zinc neutral palette
- Primary accent: emerald-500
- Font: Inter (sans), JetBrains Mono (data/mono)

## Screen 1: Project List
- Grid of cards (3-col on desktop, 1-col mobile)
- Each card: thumbnail (first storyboard frame or placeholder), title, status badge, duration, created date
- Actions: New Project (modal), Open, Delete, Download (if done)
- Empty state: illustrated upload/dropzone for script files

## Screen 2: Script Editor
- Full-width textarea with markdown-lite support
- Toolbar: template selector (YouTube Explainer, Product Demo, Social Reel), voice profile selector, character upload
- "Generate Storyboard" primary CTA
- Auto-detect scenes from paragraph breaks with live scene count
- Sidebar: project settings, character preview

## Screen 3: Storyboard View
- Vertical list of scene cards
- Each card: generated frames (grid 1x4), narration text (editable inline), visual prompt (editable), duration input
- Frame actions: select, regenerate frame, expand
- Scene actions: reorder (drag handle), delete, regenerate video
- Global actions: Back to Script, Proceed to Timeline

## Screen 4: Timeline / Preview
- Remotion player centered
- Below player: horizontal scene strip with thumbnails and durations
- Subtitle preview toggle
- Play / Pause / Seek controls
- "Render Final Video" CTA

## Screen 5: Render Queue
- List of active and completed jobs
- Progress bar with percent and stage label (e.g., "Generating scene 3/7...")
- Download button for completed jobs
- Logs accordion for debugging
