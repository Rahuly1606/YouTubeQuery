import { motion } from "framer-motion";
import { Calendar, FileVideo } from "lucide-react";

interface ResultCardProps {
  title: string;
  publishedDate: string;
  transcript: string;
  thumbnail?: string;
  index: number;
}

const ResultCard = ({ title, publishedDate, transcript, thumbnail, index }: ResultCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ scale: 1.03, y: -5 }}
      className="group relative rounded-lg overflow-hidden border border-border bg-card hover:bg-card-hover transition-all duration-300 hover:shadow-card-hover"
    >
      <div className="absolute inset-0 bg-gradient-glow opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      <div className="relative p-6">
        {thumbnail && (
          <div className="mb-4 rounded-lg overflow-hidden bg-muted">
            <img
              src={thumbnail}
              alt={title}
              className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
            />
          </div>
        )}
        
        <div className="space-y-3">
          <h3 className="text-lg font-semibold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
            {title}
          </h3>
          
          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
            <div className="flex items-center space-x-1">
              <Calendar className="w-4 h-4" />
              <span>{new Date(publishedDate).toLocaleDateString()}</span>
            </div>
            <div className="flex items-center space-x-1">
              <FileVideo className="w-4 h-4" />
              <span>Video</span>
            </div>
          </div>
          
          <p className="text-sm text-muted-foreground line-clamp-3">
            {transcript}
          </p>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="mt-4 text-sm font-medium text-primary hover:text-primary-glow transition-colors"
          >
            View Details →
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultCard;