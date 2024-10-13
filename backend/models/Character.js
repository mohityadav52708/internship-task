// backend/models/Character.js

const mongoose = require('mongoose');

const CharacterSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    role: {
        type: String,
        required: true
    },
    traits: {
        type: [String],
        required: true
    }
});

module.exports = mongoose.model('Character', CharacterSchema);
