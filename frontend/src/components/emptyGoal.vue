<script setup>
    const base_url = import.meta.env.BASE_URL
</script>

<template>
    <section class="empty-body">
        <article class="empty-left-section">
            <p> Did you have a sustainability goal in mind? </p>
            <p> Great achievements were once clearly defined goals</p>
            <button> <a :href="base_url + 'new_project'"> + Create a project </a></button>
        </article>
        <article class="empty-right-section">
            <div> <img src="../assets/images/emptyGoal.svg" alt=""></div>
        </article>
    </section>
</template>

<style scoped>
@import url("../assets/css/homepage.css");
</style>