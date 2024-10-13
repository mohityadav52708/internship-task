// backend/models/Webtoon.js

const mongoose = require('mongoose');

const WebtoonSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
        index: true
    },
    description: {
        type: String,
        required: true
    },
    characters: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Character',
        required: true
    }]
});

module.exports = mongoose.model('Webtoon', WebtoonSchema);
