import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import SearchBar from "../components/SearchBar";
import ResultCard from "../components/ResultCard";
import LoadingSpinner from "../components/LoadingSpinner";

const Search = () => {
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Mock search results
  const mockResults = [
    {
      id: 1,
      title: "Building AI Applications with Semantic Search",
      publishedDate: "2024-01-15",
      transcript: "In this comprehensive tutorial, we explore the fundamentals of semantic search and how it revolutionizes the way we find information. Learn about vector embeddings, similarity metrics, and practical implementation strategies.",
      thumbnail: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=500&h=300&fit=crop",
    },
    {
      id: 2,
      title: "Natural Language Processing Explained",
      publishedDate: "2024-02-10",
      transcript: "Dive deep into NLP concepts and understand how machines process human language. We cover tokenization, embeddings, transformers, and real-world applications in modern AI systems.",
      thumbnail: "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=500&h=300&fit=crop",
    },
    {
      id: 3,
      title: "The Future of Search Technology",
      publishedDate: "2024-03-05",
      transcript: "Exploring cutting-edge search technologies and their impact on information retrieval. From traditional keyword matching to advanced semantic understanding, see how search is evolving.",
      thumbnail: "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=500&h=300&fit=crop",
    },
    {
      id: 4,
      title: "Machine Learning for Beginners",
      publishedDate: "2024-01-20",
      transcript: "Start your journey into machine learning with this beginner-friendly guide. We cover basic concepts, algorithms, and practical examples to help you understand the fundamentals.",
      thumbnail: "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=500&h=300&fit=crop",
    },
    {
      id: 5,
      title: "Vector Databases and Embeddings",
      publishedDate: "2024-02-28",
      transcript: "Learn about vector databases and how they enable semantic search at scale. Understanding embeddings, similarity search, and practical implementation with modern tools.",
      thumbnail: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=500&h=300&fit=crop",
    },
    {
      id: 6,
      title: "AI Ethics and Responsible Development",
      publishedDate: "2024-03-12",
      transcript: "Important discussion on ethical considerations in AI development. Covering bias, fairness, transparency, and best practices for building responsible AI systems.",
      thumbnail: "https://images.unsplash.com/photo-1531746790731-6c087fecd65a?w=500&h=300&fit=crop",
    },
  ];

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setHasSearched(true);
    
    // Simulate API call
    setTimeout(() => {
      setSearchResults(mockResults);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen pt-20 pb-10">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl mx-auto text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              Semantic Search
            </span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Find YouTube videos using natural language queries
          </p>
        </motion.div>

        <div className="mb-12">
          <SearchBar onSearch={handleSearch} />
        </div>

        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex justify-center py-20"
            >
              <LoadingSpinner />
            </motion.div>
          ) : searchResults.length > 0 ? (
            <motion.div
              key="results"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="mb-6">
                <p className="text-muted-foreground">
                  Found {searchResults.length} results
                </p>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {searchResults.map((result, index) => (
                  <ResultCard
                    key={result.id}
                    title={result.title}
                    publishedDate={result.publishedDate}
                    transcript={result.transcript}
                    thumbnail={result.thumbnail}
                    index={index}
                  />
                ))}
              </div>
            </motion.div>
          ) : hasSearched ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-20"
            >
              <p className="text-muted-foreground">No results found. Try a different search query.</p>
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-20"
            >
              <p className="text-muted-foreground">
                Start searching to discover relevant videos
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default Search;