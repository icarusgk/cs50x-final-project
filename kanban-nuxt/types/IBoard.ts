import ICard from "./ICard";

export default interface IBoard {
  id: number
  name: string
  cards: ICard[]
}