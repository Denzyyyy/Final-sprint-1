const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

const API_BASE = 'http://127.0.0.1:5000/api/books';

app.get('/', async (req, res) => {
  const response = await axios.get(`${API_BASE}/all`);
  res.render('index', { books: response.data });
});

app.get('/create', (req, res) => {
  res.render('create');
});

app.post('/create', async (req, res) => {
  await axios.post(API_BASE, req.body);
  res.redirect('/');
});

app.get('/edit/:id', async (req, res) => {
  const all = await axios.get(`${API_BASE}/all`);
  const book = all.data.find(b => b.id == req.params.id);
  res.render('edit', { book });
});

app.post('/edit/:id', async (req, res) => {
  await axios.put(`${API_BASE}/${req.params.id}`, req.body);
  res.redirect('/');
});

app.post('/delete/:id', async (req, res) => {
  await axios.delete(`${API_BASE}/${req.params.id}`);
  res.redirect('/');
});

app.listen(PORT, () => console.log(`Frontend running at http://localhost:${PORT}`));
