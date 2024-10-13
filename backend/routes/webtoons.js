// backend/routes/webtoons.js

const express = require('express');
const router = express.Router();
const Webtoon = require('../models/Webtoon');
const Character = require('../models/Character');
const authenticateJWT = require('../middleware/auth');
const Joi = require('joi');

// Input validation schema using Joi
const webtoonSchema = Joi.object({
    title: Joi.string().required(),
    description: Joi.string().required(),
    characters: Joi.array().items(
        Joi.object({
            name: Joi.string().required(),
            role: Joi.string().required(),
            traits: Joi.array().items(Joi.string()).required()
        })
    ).required()
});

// GET /webtoons - Fetch all webtoons with basic details
router.get('/', async (req, res) => {
    try {
        const webtoons = await Webtoon.find().populate('characters', 'name role');
        res.json(webtoons);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// POST /webtoons - Add a new webtoon entry
router.post('/', authenticateJWT, async (req, res) => {
    // Validate input
    const { error } = webtoonSchema.validate(req.body);
    if (error) return res.status(400).json({ message: error.details[0].message });

    try {
        const { title, description, characters } = req.body;
        const characterIds = [];

        for (let char of characters) {
            const newChar = new Character(char);
            await newChar.save();
            characterIds.push(newChar._id);
        }

        const newWebtoon = new Webtoon({ title, description, characters: characterIds });
        await newWebtoon.save();
        res.status(201).json(newWebtoon);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// GET /webtoons/:id - Fetch a specific webtoon by its ID
router.get('/:id', async (req, res) => {
    try {
        const webtoon = await Webtoon.findById(req.params.id).populate('characters');
        if (!webtoon) return res.status(404).json({ message: 'Webtoon not found' });
        res.json(webtoon);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// DELETE /webtoons/:id - Remove a webtoon entry by its ID
router.delete('/:id', authenticateJWT, async (req, res) => {
    try {
        const webtoon = await Webtoon.findByIdAndDelete(req.params.id);
        if (!webtoon) return res.status(404).json({ message: 'Webtoon not found' });

        // Optionally, delete associated characters
        await Character.deleteMany({ _id: { $in: webtoon.characters } });

        res.json({ message: 'Webtoon deleted successfully' });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
