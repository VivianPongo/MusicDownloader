<template>
  <main class="main-content">
    <h1>Bienvenido a MusicDownloader</h1>
    <p class="subtitle">Descarga tu música favorita fácilmente</p>

    <div class="input-container">
      <input
        type="text"
        placeholder="Pegar enlace aquí"
        v-model="url"
        class="link-input"
      />
      <button class="download-btn" @click="startDownload">Iniciar descarga</button>
    </div>

    <div class="select_format">
      <p>Selecciona un formato</p>

      <label>
        <input type="radio" name="formato" value="mp3" v-model="formato" />
        MP3
      </label>

      <label>
        <input type="radio" name="formato" value="mp4" v-model="formato" />
        MP4
      </label>

      <label>
        <input type="radio" name="formato" value="ambos" v-model="formato" />
        Ambos
      </label>
    </div>

    <!-- Opciones avanzadas -->
    <div class="advanced-options">
      <p class="toggle-text" @click="mostrarAvanzado = !mostrarAvanzado">
        Opciones avanzadas
      </p>

      <div v-if="mostrarAvanzado" class="quality-options">
        <p>Calidad de descarga</p>

        <label>
          <input type="radio" name="calidad" value="128" v-model="calidad" />
          Baja
        </label>

        <label>
          <input type="radio" name="calidad" value="192" v-model="calidad" />
          Media
        </label>

        <label>
          <input type="radio" name="calidad" value="320" v-model="calidad" />
          Alta
        </label>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'

const url = ref('')
const formato = ref('mp3')
const calidad = ref('192')
const mostrarAvanzado = ref(false)

const startDownload = () => {
  if (!url.value.trim()) {
    alert('Por favor, pega un enlace primero.')
    return
  }

  const formData = new FormData()
  formData.append('url', url.value)
  formData.append('formato', formato.value)
  formData.append('calidad', calidad.value)

  // Agregado para debug
  for (let [key, value] of formData.entries()) {
    console.log(`${key}: ${value}`);
  }

  fetch('https://601314dd-e30d-42e3-9a5d-e67206b4fbeb-00-a7et60ztyy9p.picard.replit.dev:8080/download', {
    method: 'POST',
    body: formData,
  })
     .then(response => {
  if (!response.ok) {
    throw new Error('Hubo un error en la descarga.')
  }

  // Leer filename del header (si está disponible)
  const disposition = response.headers.get('Content-Disposition')
  let filename = ' '

  if (disposition) {
  const match = disposition.match(/filename\*=UTF-8''(.+)|filename="?([^\";]+)"?/)
  if (match) {
    filename = decodeURIComponent(match[1] || match[2])
  }}
  
  else {
    // Si no hay header (como ocurre en Replit), generar uno manual
    const titleFromURL = url.value.split('v=')[1]?.substring(0, 8) || 'audio'
    filename = `${titleFromURL}.${formato.value}`
  }

  return response.blob().then(blob => ({ blob, filename }))
})
.then(({ blob, filename }) => {
  const downloadUrl = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = downloadUrl
  a.style.display = 'none'
  a.setAttribute('download', filename)  // Asegura el nombre de archivo
  document.body.appendChild(a)
  a.click()
  a.remove()
  URL.revokeObjectURL(downloadUrl)
})
  
}
</script>



<style scoped>
.advanced-options {
  margin-top: 2rem;
}

.toggle-text {
  color: #555; /* gris oscuro, no negro puro */
  cursor: pointer;
  /*text-decoration: underline;*/
  margin-bottom: 0.5rem;
}

.quality-options {
  padding: 1rem 0;
}

.quality-options label {
  margin: 0.3rem 0;
}



.main-content {
  padding-top: 6rem; /* espacio para navbar fija */
  padding-bottom: 4rem; /* espacio para footer */
  text-align: center;
  color: #333;
}

.subtitle {
  margin-bottom: 2rem;
  color: #666;
}

.input-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.link-input {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  width: 300px;
  max-width: 90%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.download-btn {
  padding: 0.75rem 1.2rem;
  font-size: 1rem;
  background-color: #fb923c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.download-btn:hover {
  background-color: #f97316;
}

.select_format{
    padding: 0.75rem 1.2rem;
}
</style>
