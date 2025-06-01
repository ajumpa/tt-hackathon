import "dotenv/config";
import { openai, createAgent, createNetwork, createTool, Tool } from "@inngest/agent-kit";
import { createServer } from "@inngest/agent-kit/server";
import { z } from "zod";

export interface Character {
  name: string;
  traits: string[]
  locations: string[]
  elements?: string[]
}

export interface AgentState {
  story: string;
  //extract the characters first.
  characters?: Character[];

  //map character names to URLs
  images?: {
    [character: string]: string;
  }
}

const CharacterClassifier = createAgent<AgentState>({
  name: "story character classifier",
  description: "Reads a short story and identifies the characters and their attributes",
  //TODO: Switch out model for one running on tentorrent.
  model: openai({
    model: "meta-llama/Llama-3.1-8B-Instruct",
    baseUrl: "https://disciplinary-sibella-nayadaur-c5543355.koyeb.app/v1",
    
  }),
  system: ({ network }) => `
  Refer to this story:
  
  <story>
  ${network?.state.data.story}
  </story>

  Extract the characters and their traits, locations, and magical elements (if any) from the story using the "extract_characters" tool
  `,

  tools: [
    createTool({
      name: "extract_characters",
      // An array of literary characters from the story
      parameters: z.array(
        z.object({
          name: z.string(),
          traits: z.array(z.string()),
          locations: z.array(z.string()),
          elements: z.array(z.string()).optional(),
        })
      ),

      handler: async(characters: Character[], { network }) => {
        network.state.data.characters = characters;
      }
    }),
  ]

})

const storyNetwork = createNetwork<AgentState>({
  name: "Story Analysts",
  agents: [CharacterClassifier],
  router: async (opts) => {
    const { network, input } = opts;

    // always set the story.
    network.state.data.story = input;

    if (!network.state.data.characters) {
      return CharacterClassifier;
    } 
    // else if (network.state.data.security_agent_answer && network.state.data.dba_agent_answer) {
    //   return;
    // }
    return undefined;
  },
});

const server = createServer({
  agents: [],
  networks: [storyNetwork],
});

server.listen(3010, () => console.log("Agent kit running!"));
