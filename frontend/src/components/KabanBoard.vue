<script setup>
    import { ref, onMounted, watch } from "vue";
    import SprintStatus from "../components/SprintStatus.vue";
    import { useRoute } from "vue-router";
    import axios from 'axios';

    const route = useRoute();

    const app_container = ref(null);

    // Backend base URL from environment variables
    const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

    const model = ref({
        data: {
            status: [
                { id: 1, order: 1, title: "To do" },
                { id: 2, order: 2, title: "In progress" },
                { id: 3, order: 3, title: "Under review" },
                { id: 4, order: 4, title: "Completed" },
            ],
            cards: [],
            sprint: ""
        },
    });

    function convert_status_to_id(status){
        const statusMap = {
            "to_do": 1,
            "in_progress": 2,
            "under_review": 3,
            "completed": 4,
        };
        return statusMap[status] || null;
    };

    async function get_sprint(sprint_id) {
        try {
            const response = await axios.get(`${backendBaseUrl}/susaf/sprints/${sprint_id}`);
            console.log(response);
            model.value.data.sprint = response.data;
            console.log("Sprint fetched successfully:", model.value.data.sprint);
        } catch (error) {
            console.error(error);
            alert("Failed to fetch sprint: " + error.message);
        }
    }

    async function get_tasks(sprint_id) {
        try {
            const response = await axios.get(`${backendBaseUrl}/susaf/sprints/${sprint_id}/tasks/`);
            console.log(response);
            model.value.data.cards = response.data.map(task => ({
                id: task.id,
                title: task.title,
                status_id: convert_status_to_id(task.status),
                impact: Array.isArray(task.impact) 
                    ? task.impact.map(impactItem => impactItem.replace(/\b\w/g, char => char.toUpperCase())).join(', ') 
                    : task.impact.replace(/\b\w/g, char => char.toUpperCase()),
            }));

            console.log("Tasks fetched successfully:", model.value.data.cards.length);
        } catch (error) {
            console.error(error);
            alert("Failed to fetch tasks: " + error.message);
        }
    }

    function fetchData() {
        const sprint_id = route.params.id;
        if (sprint_id) {
            get_sprint(sprint_id);
            get_tasks(sprint_id);
        }
    }

    watch(
        () => route.params.sprint_id,
        (newSprintId, oldSprintId) => {
            if (newSprintId !== oldSprintId) {
                fetchData();
            }
        }
    );

    watch(
        () => route.params.id,
        (newId) => {
            if (newId) {
                fetchData();
            }
        }
    );

    onMounted(() => {
        fetchData();
    });

    function moveCard({ card_id, from_status, to_status }) {
        const card = model.value.data.cards.find((c) => c.id == card_id);
        if (card) {
            card.status_id = to_status;
        }
    }

    onMounted(() => {
        model.value.data.status.sort((a, b) => a.order - b.order);
    });
</script>

<template>
    <section>
        <section class="goal-header">
            <div class="header-left">
                <div class="goal-title"> {{model.data.sprint.title }} Sprint </div>
            </div>
        </section>

        <section class="app-container" id="app-container" ref="app_container">      
            <SprintStatus 
                v-for="item in model.data.status"
                :key="item.id"
                :status_id="item.id"
                :status_key="item.id"
                :status_item="item"
                :items_count="model.data.status.length"
                :cards="model.data.cards.filter(card => card.status_id === item.id)"
                @move_card="moveCard"
            />
        </section>
    </section>
</template>

<style scoped>
    @import url("../assets/css/kanban.css");

    .app-container {
        display: flex;
        gap: 25px;
        overflow-x: auto;
        padding: 20px;
    }
</style>