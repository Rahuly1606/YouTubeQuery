import { motion } from "framer-motion";
import { Code, Database, Cpu, Layers } from "lucide-react";

const About = () => {
  const technologies = [
    {
      icon: Code,
      name: "Next.js",
      description: "Modern React framework for production",
    },
    {
      icon: Layers,
      name: "Tailwind CSS",
      description: "Utility-first CSS framework",
    },
    {
      icon: Cpu,
      name: "Sentence Transformers",
      description: "State-of-the-art semantic search models",
    },
    {
      icon: Database,
      name: "Vector Database",
      description: "Efficient similarity search at scale",
    },
  ];

  return (
    <div className="min-h-screen pt-20 pb-10">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl mx-auto"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-center mb-8">
            About <span className="bg-gradient-primary bg-clip-text text-transparent">QueryTube</span>
          </h1>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="prose prose-lg max-w-none mb-12"
          >
            <div className="bg-card border border-border rounded-lg p-8 mb-8">
              <h2 className="text-2xl font-semibold mb-4 text-foreground">Our Mission</h2>
              <p className="text-muted-foreground leading-relaxed">
                QueryTube revolutionizes how people search for video content. By leveraging advanced 
                AI and semantic search technology, we enable users to find exactly what they're 
                looking for using natural language queries. No more struggling with keywords or 
                complex search operators – just ask in your own words, and we'll find the most 
                relevant content for you.
              </p>
            </div>

            <div className="bg-card border border-border rounded-lg p-8 mb-8">
              <h2 className="text-2xl font-semibold mb-4 text-foreground">How It Works</h2>
              <p className="text-muted-foreground leading-relaxed mb-4">
                Our platform uses state-of-the-art natural language processing to understand the 
                intent behind your queries. We analyze video transcripts, descriptions, and metadata 
                to create semantic embeddings that capture the true meaning of content.
              </p>
              <p className="text-muted-foreground leading-relaxed">
                When you search, we convert your query into the same semantic space and find videos 
                with the closest meaning – not just matching keywords. This approach delivers more 
                accurate and relevant results than traditional search methods.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="mb-12"
          >
            <h2 className="text-2xl font-semibold text-center mb-8">Built With Modern Technology</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {technologies.map((tech, index) => (
                <motion.div
                  key={tech.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.1 * index }}
                  whileHover={{ scale: 1.05 }}
                  className="bg-card border border-border rounded-lg p-6 text-center hover:border-primary/50 transition-all duration-300"
                >
                  <div className="mb-4 inline-flex p-3 rounded-lg bg-gradient-primary">
                    <tech.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="font-semibold mb-2 text-foreground">{tech.name}</h3>
                  <p className="text-sm text-muted-foreground">{tech.description}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="text-center bg-gradient-primary rounded-lg p-8 text-white"
          >
            <h2 className="text-2xl font-semibold mb-4">Ready to Experience the Future of Search?</h2>
            <p className="mb-6 opacity-90">
              Join thousands of users who are already discovering content more efficiently with QueryTube.
            </p>
            <motion.a
              href="/search"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-block px-8 py-3 bg-white text-primary rounded-full font-semibold hover:shadow-lg transition-all duration-300"
            >
              Try It Now
            </motion.a>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
};

export default About;