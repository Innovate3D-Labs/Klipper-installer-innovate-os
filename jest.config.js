module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['js', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.js$': 'babel-jest'
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/frontend/$1'
  },
  testMatch: [
    '**/tests/frontend/**/*.spec.js'
  ],
  collectCoverage: true,
  collectCoverageFrom: [
    'src/frontend/**/*.{js,vue}',
    '!src/frontend/main.js'
  ],
  coverageReporters: ['text', 'html'],
  setupFiles: ['<rootDir>/tests/frontend/setup.js']
}
