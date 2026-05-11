import '@testing-library/jest-dom'

// Mock geolocation
global.navigator.geolocation = {
  getCurrentPosition: (success, error) => {
    success({
      coords: {
        latitude: 42.3401,
        longitude: -8.3885,
        accuracy: 10,
      },
    })
  },
}

// Mock matchMedia
global.window.matchMedia = (query) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: () => {},
  removeListener: () => {},
  addEventListener: () => {},
  removeEventListener: () => {},
  dispatchEvent: () => {},
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
}
