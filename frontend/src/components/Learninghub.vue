<script setup>
import Navbar from '../components/navbar.vue';
import { ref, computed } from 'vue';
import PostCard from './PostCard.vue';

// Sample posts with categories
const posts = ref([
  {
    id: 0,
    title: "SUSAF Overview",
    link: "https://www.youtube.com/watch?v=5iPUtG5WqFQ",
    type: "Video",
    description: "An overview of SUSAF.",
    category: "Sustainability",
  },
  {
    id: 1,
    title: "Advantages of using SUSAF",
    link: "https://www.youtube.com/watch?v=tkM6aEXupko",
    type: "Video",
    description: "Short video about the advantages of using SUSAF.",
    category: "Sustainability",
  },
  {
    id: 2,
    title: "GreenCode Foundation",
    link: "https://www.greencode.foundation",
    type: "Link",
    description: "Explore the GreenCode Foundation's mission and projects on sustainability in tech.",
    category: "Sustainability",
  },
  {
    id: 3,
    title: "Sustainability in Software Development - Video",
    link: "https://www.youtube.com/watch?v=z89NggcQpf0",
    type: "Video",
    description: "A video discussing sustainability practices in software engineering.",
    category: "Software Engineering",
  },
  {
    id: 4,
    title: "Learning Resource on Agile and Sustainability",
    link: "https://instituteprojectmanagement.com/blog/sustainability-in-agile-project-management/",
    type: "Link",
    description: "Learn how to integrate sustainability in Agile frameworks.",
    category: "Sustainability",
  },
  {
    id: 5,
    title: "AI and Climate Change Solutions",
    link: "https://www.youtube.com/watch?v=SLTqYDTJ1Go",
    type: "Link",
    description: "How AI can play a key role in tackling climate change.",
    category: "AI for Environment",
  },
  {
    id: 6,
    title: "Tech for Good - Video",
    link: "https://www.youtube.com/watch?v=rLuCN5itJPo",
    type: "Video",
    description: "A talk about how technology is being used to improve the environment.",
    category: "Technology for Good",
  },
  {
    id: 7,
    title: "Agile for Sustainability - Webinar",
    link: "https://instituteprojectmanagement.com/blog/sustainability-in-agile-project-management/",
    type: "Link",
    description: "Webinar on applying Agile practices in sustainable development.",
    category: "Sustainability",
  }
]);

const postsPerPage = 3; // Define how many posts you want to display per page
const currentPage = ref(1); // Track the current page
const selectedCategory = ref('All'); // Track the selected category
const searchQuery = ref(''); // Search query

// Filter posts based on selected category and search query
const filteredPosts = computed(() => {
  let result = posts.value.filter(post => {
    return selectedCategory.value === 'All' || post.category === selectedCategory.value;
  });

  if (searchQuery.value) {
    result = result.filter(post => post.title.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }

  return result;
});

// Computed property to get the paginated posts
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * postsPerPage;
  const end = start + postsPerPage;
  return filteredPosts.value.slice(start, end);
});

// Computed property to calculate the total number of pages
const totalPages = computed(() => {
  return Math.ceil(filteredPosts.value.length / postsPerPage);
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}

function changeCategory(category) {
  selectedCategory.value = category;
  currentPage.value = 1; // Reset to the first page when changing category
}

// FAQ Data and Filter
const faqs = ref([
  {
    question: 'What is SusAF?',
    answer: 'SusAF, or the Sustainability Awareness Framework, is a structured approach that helps software teams integrate sustainability considerations into their Agile development processes.'
  },
  {
    question: 'Why is sustainability important in software development?',
    answer: 'Sustainability in software development ensures that products not only perform efficiently but also reduce negative environmental, social, and economic impacts throughout their lifecycle.'
  },
  {
    question: 'How does SusAF integrate into Agile processes?',
    answer: 'SusAF is designed to fit seamlessly into Scrum by helping teams assess and address sustainability in each sprint, from planning to retrospectives, ensuring that sustainability is embedded in every decision.'
  },
  {
    question: 'What are the main steps in the SusAF process?',
    answer: 'The main steps in SusAF are: Warm-Up (introduce sustainability), Capture (identify impacts), Analyze (assess cause and effect), Synthesis (plan actions), Sustainability Update (track during development), and Reflection (review in sprint retrospectives).'
  },
  {
    question: 'How can I get started with Agile and Sustainability?',
    answer: 'You can start by exploring Agile methodologies and how they can be integrated with sustainability goals. Many courses and resources are available in the Learning Hub.',
  },
  {
    question: 'What is sustainable software development?',
    answer: 'Sustainable software development involves creating software that minimizes environmental impact, such as energy consumption, and reduces waste.',
  },
  {
    question: 'What is AI\'s role in climate change solutions?',
    answer: 'AI can analyze large amounts of data to find patterns, optimize resource usage, and assist in climate change modeling and prediction.',
  },
  // Add more FAQs as needed
]);

const searchFaq = ref('');
const filteredFaqs = computed(() => {
  return faqs.value.filter(faq =>
    faq.question.toLowerCase().includes(searchFaq.value.toLowerCase())
  );
});
</script>

<template>
  <section class="container">
    <Navbar />
    <div class="learning-hub">
      <h1>Welcome to the Learning Hub</h1>

      <!-- Search Bar for Posts -->
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search posts..."
          class="input-search"
        />
      </div>

      <!-- Category Filter -->
      <div class="category-filter">
        <button @click="changeCategory('All')">All</button>
        <button @click="changeCategory('Sustainability')">Sustainability</button>
        <button @click="changeCategory('Software Engineering')">Software Engineering</button>
        <button @click="changeCategory('AI for Environment')">AI for Environment</button>
        <button @click="changeCategory('Technology for Good')">Technology for Good</button>
      </div>

      <!-- Posts -->
      <div class="posts-container">
        <PostCard
          v-for="post in paginatedPosts"
          :key="post.id"
          :title="post.title"
          :link="post.link"
          :type="post.type"
          :description="post.description"
        />
      </div>

      <!-- Pagination Controls -->
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>

      <!-- FAQ Section -->
      <div class="faq-section">
        <h2>Frequently Asked Questions</h2>
        <input v-model="searchFaq" type="text" placeholder="Search FAQ..." class="faq-search-bar" />

        <div v-if="filteredFaqs.length === 0" class="no-results">
          No results found. Try a different search term.
        </div>

        <div v-for="faq in filteredFaqs" :key="faq.question" class="faq-card">
          <h3>{{ faq.question }}</h3>
          <p>{{ faq.answer }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Layout and Spacing */
.container {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 20px;
}

.learning-hub {
  max-width: 1200px;
  margin: 0 auto;
}

.learning-hub h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 30px;
  text-align: center;
  color: #333;
}

/* Search Bar */
.input-search {
  padding: 12px 20px;
  font-size: 16px;
  width: 100%;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

/* Category Filter */
.category-filter {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.category-filter button {
  padding: 12px 20px;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.category-filter button:hover {
  background-color: #45a049;
}

/* Posts Container */
.posts-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 40px;
}

.pagination button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.pagination button:hover {
  background-color: #45a049;
}

.pagination button:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
}

.pagination span {
  font-size: 18px;
  font-weight: 500;
}

/* FAQ Section */
.faq-section {
  margin-top: 40px;
}

.faq-search-bar {
  padding: 12px 20px;
  font-size: 16px;
  width: 100%;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
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
