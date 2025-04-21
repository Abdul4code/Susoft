import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios  from 'axios'

export const useStateStore = defineStore("state", () => {
    // State
    const state = ref({
        project_id: null,
        current_sprint: null,
    });


    // Actions
    const saveProjectId = (id) => {
        state.value.project_id = id;
    };

    const saveSprint = (sprint_id) => {
        state.value.current_sprint = sprint_id;
    }


    return {
        state,
        saveProjectId,
        saveSprint
    };
});