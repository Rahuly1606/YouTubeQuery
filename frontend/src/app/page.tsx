'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { MagnifyingGlassIcon, PlayIcon, ClockIcon, EyeIcon } from '@heroicons/react/24/outline';
import { searchVideos } from '../services/api';
import type { SearchResult } from '@/types';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

export default function Home() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const response = await searchVideos({ query, top_k: 10 });
      setResults(response.results);
      setHasSearched(true);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDuration = (duration: string | undefined) => {
    if (!duration) return '0:00';
    // Convert ISO 8601 duration to readable format
    const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
    if (!match) return duration;

    const hours = match[1] ? `${match[1]}:` : '';
    const minutes = match[2] ? match[2].padStart(hours ? 2 : 1, '0') : '0';
    const seconds = match[3] ? match[3].padStart(2, '0') : '00';

    return `${hours}${minutes}:${seconds}`;
  };

  const formatViews = (views: string | number | undefined) => {
    if (!views) return '0';
    const num = typeof views === 'string' ? parseInt(views) : views;
    if (isNaN(num)) return '0';
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 pt-16">
        <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <PlayIcon className="w-8 h-8 text-red-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-800 dark:text-white">
              QueryTube
            </h1>
          </div>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Search YouTube videos using AI-powered semantic search.
            Find content by meaning, not just keywords.
          </p>
        </motion.div>

        {/* Search Form */}
        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          onSubmit={handleSearch}
          className="max-w-2xl mx-auto mb-12"
        >
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for videos... (e.g., 'machine learning tutorials', 'cooking recipes')"
              className="w-full px-6 py-4 pr-14 text-lg border border-gray-300 rounded-xl 
                       focus:ring-2 focus:ring-red-500 focus:border-transparent 
                       dark:bg-gray-800 dark:border-gray-600 dark:text-white
                       shadow-lg transition-all duration-200"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="absolute right-2 top-1/2 transform -translate-y-1/2
                       bg-red-600 hover:bg-red-700 disabled:bg-gray-400
                       text-white p-3 rounded-lg transition-colors duration-200
                       disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <MagnifyingGlassIcon className="w-5 h-5" />
              )}
            </button>
          </div>
        </motion.form>

        {/* Results */}
        {hasSearched && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="max-w-6xl mx-auto"
          >
            {results.length > 0 ? (
              <>
                <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6">
                  Search Results ({results.length})
                </h2>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                  {results.map((result, index) => (
                    <motion.div
                      key={result.video_id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden
                               hover:shadow-xl transition-shadow duration-300"
                    >
                      {/* Thumbnail */}
                      <div className="relative aspect-video bg-gray-200 dark:bg-gray-700">
                        <img
                          src={result.thumbnail_url}
                          alt={result.title}
                          className="w-full h-full object-cover"
                        />
                        <div className="absolute bottom-2 right-2 bg-black bg-opacity-75 text-white 
                                      text-xs px-2 py-1 rounded flex items-center">
                          <ClockIcon className="w-3 h-3 mr-1" />
                          {formatDuration(result.duration)}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="p-4">
                        <h3 className="font-semibold text-gray-800 dark:text-white mb-2 line-clamp-2">
                          {result.title}
                        </h3>

                        <p className="text-sm text-gray-600 dark:text-gray-300 mb-3 line-clamp-2">
                          {result.description}
                        </p>

                        <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                          <span className="font-medium">{result.channel}</span>
                          <div className="flex items-center">
                            <EyeIcon className="w-4 h-4 mr-1" />
                            {formatViews(result.view_count)}
                          </div>
                        </div>

                        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                          <div className="flex items-center justify-between">
                            <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded-full">
                              {((result.score || 0) * 100).toFixed(1)}% match
                            </span>
                            <a
                              href={`https://youtube.com/watch?v=${result.video_id}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-red-600 hover:text-red-700 font-medium text-sm
                                       flex items-center transition-colors duration-200"
                            >
                              <PlayIcon className="w-4 h-4 mr-1" />
                              Watch
                            </a>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <MagnifyingGlassIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-2">
                  No results found
                </h3>
                <p className="text-gray-500 dark:text-gray-400">
                  Try a different search query or check that the backend is running with data.
                </p>
              </div>
            )}
          </motion.div>
        )}

        {/* Getting Started */}
        {!hasSearched && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="max-w-4xl mx-auto text-center"
          >
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6">
              Getting Started
            </h2>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
                <div className="w-12 h-12 bg-red-100 text-red-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-xl font-bold">1</span>
                </div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-2">
                  Collect Data
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Run the data pipeline to collect YouTube videos and transcripts
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
                <div className="w-12 h-12 bg-red-100 text-red-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-xl font-bold">2</span>
                </div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-2">
                  Generate Embeddings
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Create AI embeddings and build the searchable index
                </p>
              </div>

              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
                <div className="w-12 h-12 bg-red-100 text-red-600 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <span className="text-xl font-bold">3</span>
                </div>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-2">
                  Start Searching
                </h3>
                <p className="text-gray-600 dark:text-gray-300 text-sm">
                  Search for videos using natural language queries
                </p>
              </div>
            </div>
          </motion.div>
        )}
        </div>
      </div>
      <Footer />
    </>
  );
}
