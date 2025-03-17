require('dotenv').config();
const express = require('express');
const cors = require('cors');
const spotifyPreviewFinder = require('spotify-preview-finder');

const app = express();
const port = 3000;

app.use(cors());

app.get('/preview', async (req, res) => {
    const songTitle = req.query.title;

    if (!songTitle) {
        return res.status(400).json({ error: 'unprovided song title (title)' });
    }

    try {
        const result = await spotifyPreviewFinder(songTitle, 1);
        if (result.success && result.results.length > 0) {
            return res.json({ previewUrl: result.results[0].previewUrls[0] || null });
        } else {
            return res.status(404).json({ error: 'Available Preview URL Not Found' });
        }
    } catch (error) {
        return res.status(500).json({ error: 'Can not fetch available URL' });
    }
});

app.listen(port, () => {
    console.log(`Music fetch preview url runs on http://localhost:${port}`);
});
