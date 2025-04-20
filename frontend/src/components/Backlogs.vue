<script setup>
  import { ref, watch } from "vue";
  import draggable from "vuedraggable";
  import { useRoute } from 'vue-router';
  import axios from 'axios';
  import router from '@/router';

  const route = useRoute();

  const projectId = ref(route.params.id)


  // Project details
  const project = ref({
    title: "",
    description: ""
  });

  const sprints_data = ref([]);
  const task_data = ref([]);

  // Reactive state
  const sprints = ref([]);

  // Backend base URL from environment variables
  const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

  
  // process the display data for sprints and tasks
  // Watcher
  function processData (){
    console.log(sprints_data.value, task_data.value);
    for (const sprint_data of sprints_data.value) {
      const sprint = {
        id: sprint_data.id,
        name: sprint_data.title,
        editing: false,
        tasks: []
      };
      for (let i = 0; i < task_data.value.length; i++) {
        if (task_data.value[i].sprint == sprint.id) {
          const task = { id: task_data.value[i].id, name: task_data.value[i].title };
          sprint.tasks.push(task);
        }
      }
      sprints.value.push(sprint);
      console.log(sprints.value);
    }
  }

  // Watch for route changes and re-fetch data
  watch(
    () => route.params.id,
    (newId) => {
      projectId.value = parseInt(newId, 10); // Update projectId as an integer
      sprints_data.value = []; // Clear existing data
      task_data.value = [];
      sprints.value = [];
      get_project(); // Re-fetch data for the new project ID
      console.log(projectId.value)
    }
  );


  

  // Methods
  async function get_project() {
    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/projects/${projectId.value}`);
      project.value.title = response.data.name;
      project.value.description = response.data.description;

      await get_sprints(projectId.value);
    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  async function get_sprints(project_id) {

    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/sprints/`);
      for (const sprint of response.data) {
        if (sprint.project == project_id) {
          sprints_data.value.push(sprint);
          console.log(sprint.data)
        }
      }
      const resp = await get_tasks();

    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  async function get_tasks() {
    try {
      const response = await axios.get(`${backendBaseUrl}/susaf/tasks/`);
      for (const task of response.data) {
        // Loop through each sprint in sprints_data
        for (let i = 0; i < sprints_data.value.length; i++) {
          // Check if task's sprint matches the current sprint
          if (sprints_data.value[i].id == task.sprint) {
            task_data.value.push(task); // Push the task into task_data
          }
        }
      }

      processData(); // Call the function to process and display data
    } catch (error) {
      console.error(error);
      alert(error);
    }
  }

  get_project();

  const addSprint = async () => {
 
    let new_sprint = await axios.post(`${backendBaseUrl}/susaf/sprints/`, {
      title: "Untitled Sprint",
      project: projectId.value
    });

    sprints.value.push({
      id: new_sprint.data.id,
      name: new_sprint.data.title,
      editing: false,
      tasks: []
    });
  };

  const editSprint = (sprint) => {
    sprint.editing = true;
  };

  const stopEditing = async (sprint) => {
    sprint.editing = false;

    try {
      // Update the sprint in the database
      await axios.put(`${backendBaseUrl}/susaf/sprints/${sprint.id}/`, {
        title: sprint.name,
        project: projectId.value
      });
    } catch (error) {
      console.error("Error updating sprint:", error);
      alert("Failed to update the sprint. Please try again.");
    }
  };

  const goToTaskDetail = (taskId) => {
    router.push({ name: 'detail', params: { id: taskId } });
  };

  const updateTaskSprint = async (taskId, newSprintId) => {
    try {
      await axios.patch(`${backendBaseUrl}/susaf/tasks/${taskId}/`, {
        sprint: newSprintId,
      });
      console.log(`Task ${taskId} moved to sprint ${newSprintId}`);
    } catch (error) {
      console.error("Error updating task sprint:", error);
      alert("Failed to update task's sprint.");
    }
  };

  const onTaskDrop = async (event, newSprintId, event_to) => {
    
    console.log(event_to)
    const task = event.item.querySelector('.task-name'); 
    const taskId = task.id;

    const sprint = event_to.querySelector('.task');
    const sprintId = sprint.getAttribute('sprint_id');


    if (taskId && sprintId) {
      await updateTaskSprint(taskId, sprintId);
    }
  };


</script>

<template>
    <div class="container">
      <h3 class="title">{{ project.title }}</h3>
      <p class="subtitle">{{ project.description }}</p>
  
      <div v-for="sprint in sprints" :key="sprint.id" class="sprint-box">
        <!-- Editable Sprint Title -->
        <input 
          v-if="sprint.editing" 
          v-model="sprint.name" 
          @blur="stopEditing(sprint)" 
          @keyup.enter="stopEditing(sprint)"
          class="sprint-title-input"
          
        />
        <h4 v-else class="sprint-title" @click="editSprint(sprint)">{{ sprint.name }}</h4>
  
        <!-- Draggable Task List -->
        <draggable
            v-model="sprint.tasks"
            group="tasks"
            itemKey="id"
            class="task-list"

            @end="(event) => onTaskDrop(event, sprint.id, event.to)">

            <template #item="{ element: task }">
              <div class="task" :sprint_id="sprint.id" @click="goToTaskDetail(task.id)">
                <span class="task-name" :id="task.id" >{{ task.name }}</span>
              </div>
            </template>

        </draggable>
        </div>
  
      <div class="footer">
        <button class="add-sprint" @click="addSprint">+ Add New Sprint</button>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* Container */
  .container {
    width: 70%;
    margin: auto;
    padding: 30px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
    text-align: left;
  }
  
  /* Title */
  .title {
    font-size: 35px;
    color: #353535;
    font-family: "Poppins";
    font-weight: 600;
    margin-bottom: 10px;
  }
  
  .subtitle {
    margin-bottom: 50px;
  }
  
  /* Sprint Box */
  .sprint-box {
    background: linear-gradient(135deg, #ece9e6, #ffffff);
    padding: 25px;
    margin: 20px 0;
    border-radius: 10px;
    box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out;
  }
  
  .sprint-box:hover {
    transform: translateY(-5px);
  }
  
  /* Editable Sprint Title */
  .sprint-title {
    font-size: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.3s ease;
  }
  
  .sprint-title:hover {
    color: #007bff;
  }
  
  .sprint-title-input {
    font-size: 20px;
    font-weight: 600;
    width: 100%;
    border: none;
    background: none;
    outline: none;
    padding: 5px;
  }
  
  /* Task List */
  .task-list {
    min-height: 50px;
  }
  
  /* Task */
  .task {
    background: #fafafa;
    padding: 12px 15px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
    transition: background 0.3s ease-in-out;
    cursor: pointer;
  }
  
  .task:hover {
    background: #f1f1f1;
  }
  
  /* Add Sprint Button */
  .add-sprint {
    background: #007bff;
    color: white;
    font-size: 16px;
    padding: 12px 20px;
    border: none;
    cursor: pointer;
    border-radius: 8px;
    transition: background 0.3s ease-in-out;
    margin-top: 20px;
  }
  
  .add-sprint:hover {
    background: #0056b3;
  }
  </style>
