import { useState } from "react";
import { Search } from "lucide-react";
import { motion } from "framer-motion";

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

const SearchBar = ({ onSearch, placeholder = "Search videos with natural language..." }: SearchBarProps) => {
  const [query, setQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className={`relative w-full max-w-2xl mx-auto transition-all duration-300 ${
        isFocused ? "scale-105" : ""
      }`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div
        className={`relative rounded-full overflow-hidden transition-all duration-300 ${
          isFocused
            ? "shadow-glow ring-2 ring-primary"
            : "shadow-lg hover:shadow-xl"
        }`}
      >
        <div className="absolute inset-0 bg-gradient-primary opacity-10" />
        <div className="relative flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={placeholder}
            className="w-full px-6 py-4 pl-14 bg-background/90 backdrop-blur-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
          />
          <Search className="absolute left-5 w-5 h-5 text-muted-foreground pointer-events-none" />
          <motion.button
            type="submit"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="absolute right-2 px-6 py-2 bg-gradient-primary text-white rounded-full font-medium hover:shadow-glow transition-all duration-300"
          >
            Search
          </motion.button>
        </div>
      </div>
    </motion.form>
  );
};

export default SearchBar;