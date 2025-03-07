<script setup>
import { defineProps } from "vue";

const props = defineProps({
  title: String,
  link: String,
  type: String,
  description: String,
});

function extractYouTubeId(url) {
  const regex = /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
  const match = url.match(regex);
  return match ? match[1] : null;
}

const videoId = extractYouTubeId(props.link);
const thumbnailUrl = videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : '';
</script>

<template>
  <div class="post-card">
    <h2>{{ title }}</h2>
    <p>{{ description }}</p>
    <a :href="link" target="_blank" :class="{ 'is-video': type === 'Video' }">
      <div v-if="type === 'Video' && thumbnailUrl" class="video-thumbnail">
        <img :src="thumbnailUrl" alt="Video Thumbnail" />
      </div>
      {{ type === 'Video' ? 'Watch Video' : 'Visit Link' }}
    </a>
  </div>
</template>

<style scoped>
.post-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.post-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.post-card h2 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.post-card p {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
}

.post-card a {
  text-decoration: none;
  color: #4CAF50;
  font-weight: 500;
  font-size: 16px;
}

.post-card a.is-video {
  color: #FF5722;
}

.video-thumbnail img {
  width: 100%;
  max-height: 180px;
  border-radius: 5px;
  object-fit: cover;
  margin-bottom: 10px;
}
</style>

