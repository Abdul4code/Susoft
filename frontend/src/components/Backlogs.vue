<script setup>
  import { ref, watch  } from "vue";
  import draggable from "vuedraggable";
  import { useRoute } from 'vue-router';
  import axios from 'axios'
  import router from '@/router';

  const route = useRoute();

  const projectId = route.params.id;

  //project details
  const project = ref({
    title: "",
    description: ""
  })

  const sprints_data = ref([])
  const task_data = ref([])
  
  // Reactive state
  const sprints = ref([]);

  //watcher
watch([sprints_data, task_data], () => {
    for(const sprint_data of sprints_data.value){
        var sprint = {
            id: sprint_data.id,
            name:sprint_data.title,
            editing: false,
            tasks: [

            ]
        }
        for(var i = 0; i < task_data.value.length; i++){
            console.log(task_data.value[i].sprint, sprint.id)
            if(task_data.value[i].sprint == sprint.id){
                let task = {id:task_data.value[i].id, name:task_data.value[i].title}
                sprint.tasks.push(task)
            }
        }
    }
    sprints.value.push(sprint)
}, { deep: true });
  
  // Methods
 function get_project(){

    axios.get(`http://129.213.86.120:8000/susaf/projects/${projectId}`)
        .then(function (response) {
            project.value.title = response.data.name
            project.value.description = response.data.description

            get_sprints(projectId)

            console.log(sprints)

            
        })
        .catch(function (error) {
            console.log(error)
            alert(error)
        });
 }

 function get_sprints(project_id){
    axios.get(`http://129.213.86.120:8000/susaf/sprints/`)
        .then(function (response) {
            for (const sprint of response.data) {
                if(sprint.project == project_id){
                    sprints_data.value.push(sprint)
                } 
            }
            console.log(sprints_data)
            let resp = get_tasks()
            if(!resp || resp.length < 1 ) {
                setTimeout(() => {resp = get_tasks()} ,10000)
            }
        })
        .catch(function (error) {
            console.log(error)
            alert(error)
        });
 }

 function get_tasks() {
    axios.get('http://129.213.86.120:8000/susaf/tasks/')
        .then(function (response) {
            for (const task of response.data) {
                // Loop through each sprint in sprints_data
                for (var i = 0; i < sprints_data.value.length; i++) {     
                    // Check if task's sprint matches the current sprint
                    if (sprints_data.value[i].id == task.sprint) {
                        task_data.value.push(task);  // Push the task into task_data
                    }
                }
            }

            console.log(sprints_data)

        })
        .catch(function (error) {
            console.error(error);  // Log the error
            alert(error);  // Show an alert with the error message
        });
}

 get_project()

  const addSprint = () => {
    sprints_data.value.push({
      id: Date.now(),
      project: projectId,
      title: "Untitled Sprint"
    });
  };
  
  const editSprint = (sprint) => {
    sprint.editing = true;
  };
  
  const stopEditing = (sprint) => {
    sprint.editing = false;
  };

  const goToTaskDetail = (taskId) => {
    router.push({ name: 'detail', params: { id: taskId } });
  };
  </script>

<template>
    <div class="container">
      <h3 class="title">{{project.title}}</h3>
      <p class="subtitle">{{project.description}}</p>
  
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
        <draggable v-model="sprint.tasks" group="tasks" itemKey="id" class="task-list">
          <template #item="{ element: task }">
            <div class="task" @click="goToTaskDetail(task.id)">
              <span class="task-name">{{ task.name }}</span>
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
  