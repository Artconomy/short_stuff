/** @type {import('ts-jest/dist/types').InitialOptionsTsJest} */
module.exports = {
  preset: 'ts-jest',
  roots: ["src"],
  collectCoverageFrom: ['./src/**'],
  collectCoverage: true,
  coverageThreshold: {
    global: {
      lines: 90,
    }
  },
  testMatch: [
    '**/**/*.test.ts',
  ],
  coveragePathIgnorePatterns: [
    '.*[.]spec[.]ts',
    '.*[.]d[.]ts',
    '/specs/',
    '.*[.]js',
  ]
}

