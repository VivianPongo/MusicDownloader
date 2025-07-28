<template>
  <nav class="navbar">
    <div class="container">
      <div class="logo">🎵MusicDownloader</div>

      <!-- Botón hamburguesa -->
      <button class="menu-toggle" @click="toggleMenu">
        ☰
      </button>

      <!-- Links de navegación -->
      <div :class="['nav-links', { 'open': isMenuOpen }]">
        <a href="#">Inicio</a>
        <a href="#">Descargar</a>
        <a href="#">Contacto</a>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<style scoped>
/* Barra de navegación */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(to right, #facc15, #fb923c, #facc15);
  color: white;
  padding: 1rem 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 999;
}

/* Contenedor interno */
.container {
  max-width: 90%;
  left: 0;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Menú normal */
.nav-links {
  display: flex;
  gap: 1rem;
}

/* Botón hamburguesa oculto por defecto */
.menu-toggle {
  display: none;
  font-size: 1.5rem;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
}

/* Responsive */
@media (max-width: 420px) {
  .nav-links {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 100%;
    right: 0;
    background: #fb923c;
    width: 80%;
    text-align: right;
    padding: 1rem 2rem;
  }

  .nav-links.open {
    display: flex;
  }

  .menu-toggle {
    display: block;
  }
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 0.1rem 0;
}

.nav-links a:hover {
  text-decoration: underline;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
   /* o 1rem si lo quieres más separado del borde */
}

</style>
