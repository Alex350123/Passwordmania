require('dotenv').config();
const express = require('express');
const cors = require('cors');  // 允许跨域请求
const spotifyPreviewFinder = require('spotify-preview-finder');

const app = express();
const port = 3000;

app.use(cors());  // 允许所有来源访问

app.get('/preview', async (req, res) => {
    const songTitle = req.query.title;

    if (!songTitle) {
        return res.status(400).json({ error: '请提供歌曲名称 (title)' });
    }

    try {
        const result = await spotifyPreviewFinder(songTitle, 1); // 获取最多 1 条数据
        if (result.success && result.results.length > 0) {
            return res.json({ previewUrl: result.results[0].previewUrls[0] || null });
        } else {
            return res.status(404).json({ error: '未找到可用的预览 URL' });
        }
    } catch (error) {
        return res.status(500).json({ error: '无法获取预览 URL' });
    }
});

app.listen(port, () => {
    console.log(`🎵 预览服务运行在 http://localhost:${port}`);
});
