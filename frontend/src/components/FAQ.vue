<script setup>
import { ref } from 'vue';

const faqs = ref([
  {
    question: 'What is the GreenCode Foundation?',
    answer: 'The GreenCode Foundation is focused on promoting sustainability in technology and developing eco-friendly solutions.',
  },
  {
    question: 'How can I get started with Agile and Sustainability?',
    answer: 'You can start by exploring Agile methodologies and how they can be integrated with sustainability goals. There are courses and resources available in the Learning Hub.',
  },
  {
    question: 'What are the key principles of sustainable software development?',
    answer: 'Sustainable software development focuses on reducing energy consumption, optimizing performance, and minimizing the carbon footprint of technology solutions.',
  },
  // Add more questions and answers as needed
]);

const searchQuery = ref('');
const filteredFaqs = computed(() => {
  return faqs.value.filter(faq =>
    faq.question.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});
</script>

<template>
  <div class="faq-section">
    <h2>Frequently Asked Questions</h2>
    <input v-model="searchQuery" type="text" placeholder="Search for a question..." class="search-bar" />
    
    <div v-if="filteredFaqs.length === 0" class="no-results">
      No results found. Try a different search term.
    </div>
    
    <div v-for="faq in filteredFaqs" :key="faq.question" class="faq-card">
      <h3>{{ faq.question }}</h3>
      <p>{{ faq.answer }}</p>
    </div>
  </div>
</template>

<style scoped>
.faq-section {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.search-bar {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  margin-bottom: 20px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.faq-card {
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.faq-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.faq-card p {
  font-size: 16px;
  color: #555;
}

.no-results {
  text-align: center;
  color: #ff0000;
}
</style>
