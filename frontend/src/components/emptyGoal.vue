<script setup>
</script>

<template>
    <section class="empty-body">
        <article class="empty-left-section">
            <p>Create a Goal to get Started </p>
            <p> Great achievements were once clearly defined goals</p>
            <button @click="$emit('toggle_goal_form')"> + &nbsp Create A Goal </button>
        </article>
        <article class="empty-right-section">
            <div> <img src="../assets/images/emptyGoal.svg" alt=""></div>
        </article>
    </section>
</template>

<style scoped>
@import url("../assets/css/homepage.css");
</style>