// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Definišemo šemu za blog postove
const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
    author: z.string(),
    authorBio: z.string().optional(),
    image: z.string().optional(),
    imageAlt: z.string().optional(),
    category: z.string(),
    tags: z.array(z.string()).default([]),
    readingTime: z.number(),
    excerpt: z.string(),
  })
});

// Eksportujemo kolekcije
export const collections = { blog };